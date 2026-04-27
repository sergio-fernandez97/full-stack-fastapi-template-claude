import uuid

from fastapi.testclient import TestClient
from sqlmodel import Session

from app import crud
from app.core.config import settings
from app.models import ItemCreate
from tests.utils.item import create_random_item
from tests.utils.user import create_random_user


def test_create_item(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    data = {"title": "Foo", "description": "Fighters"}
    response = client.post(
        f"{settings.API_V1_STR}/items/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == data["title"]
    assert content["description"] == data["description"]
    assert "id" in content
    assert "owner_id" in content


def test_read_item(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    item = create_random_item(db)
    response = client.get(
        f"{settings.API_V1_STR}/items/{item.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == item.title
    assert content["description"] == item.description
    assert content["id"] == str(item.id)
    assert content["owner_id"] == str(item.owner_id)


def test_read_item_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    response = client.get(
        f"{settings.API_V1_STR}/items/{uuid.uuid4()}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Item not found"


def test_read_item_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    item = create_random_item(db)
    response = client.get(
        f"{settings.API_V1_STR}/items/{item.id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 403
    content = response.json()
    assert content["detail"] == "Not enough permissions"


def test_read_items(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    create_random_item(db)
    create_random_item(db)
    response = client.get(
        f"{settings.API_V1_STR}/items/",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content["data"]) >= 2


def test_update_item(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    item = create_random_item(db)
    data = {"title": "Updated title", "description": "Updated description"}
    response = client.put(
        f"{settings.API_V1_STR}/items/{item.id}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == data["title"]
    assert content["description"] == data["description"]
    assert content["id"] == str(item.id)
    assert content["owner_id"] == str(item.owner_id)


def test_update_item_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    data = {"title": "Updated title", "description": "Updated description"}
    response = client.put(
        f"{settings.API_V1_STR}/items/{uuid.uuid4()}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Item not found"


def test_update_item_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    item = create_random_item(db)
    data = {"title": "Updated title", "description": "Updated description"}
    response = client.put(
        f"{settings.API_V1_STR}/items/{item.id}",
        headers=normal_user_token_headers,
        json=data,
    )
    assert response.status_code == 403
    content = response.json()
    assert content["detail"] == "Not enough permissions"


def test_delete_item(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    item = create_random_item(db)
    response = client.delete(
        f"{settings.API_V1_STR}/items/{item.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["message"] == "Item deleted successfully"


def test_delete_item_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    response = client.delete(
        f"{settings.API_V1_STR}/items/{uuid.uuid4()}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Item not found"


def test_delete_item_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    item = create_random_item(db)
    response = client.delete(
        f"{settings.API_V1_STR}/items/{item.id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 403
    content = response.json()
    assert content["detail"] == "Not enough permissions"


def test_read_items_search_match_on_title(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    # Use a unique suffix so this item is reliably identified across tests
    unique_suffix = uuid.uuid4().hex[:12]
    title = f"SearchableTitle-{unique_suffix}"
    owner = create_random_user(db)
    assert owner.id is not None
    crud.create_item(
        session=db,
        item_in=ItemCreate(title=title, description="some unrelated description"),
        owner_id=owner.id,
    )
    # Search using upper-case variant of the suffix to verify case-insensitivity
    response = client.get(
        f"{settings.API_V1_STR}/items/",
        headers=superuser_token_headers,
        params={"search": unique_suffix.upper()},
    )
    assert response.status_code == 200
    content = response.json()
    assert content["count"] >= 1
    ids_in_data = [item["id"] for item in content["data"]]
    # Confirm the specific item we created is present
    matching = [item for item in content["data"] if unique_suffix in item["title"].lower()]
    assert len(matching) >= 1


def test_read_items_search_match_on_description(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    unique_suffix = uuid.uuid4().hex[:12]
    description = f"SearchableDesc-{unique_suffix}"
    owner = create_random_user(db)
    assert owner.id is not None
    crud.create_item(
        session=db,
        item_in=ItemCreate(title="plain title without marker", description=description),
        owner_id=owner.id,
    )
    # Search using upper-case variant to verify case-insensitivity
    response = client.get(
        f"{settings.API_V1_STR}/items/",
        headers=superuser_token_headers,
        params={"search": unique_suffix.upper()},
    )
    assert response.status_code == 200
    content = response.json()
    assert content["count"] >= 1
    matching = [
        item for item in content["data"]
        if item["description"] and unique_suffix in item["description"].lower()
    ]
    assert len(matching) >= 1


def test_read_items_search_no_results(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    # A UUID-derived string is virtually guaranteed not to appear in any item
    guaranteed_absent = f"NOMATCH-{uuid.uuid4().hex}"
    response = client.get(
        f"{settings.API_V1_STR}/items/",
        headers=superuser_token_headers,
        params={"search": guaranteed_absent},
    )
    assert response.status_code == 200
    content = response.json()
    assert content["data"] == []
    assert content["count"] == 0


def test_read_items_search_empty_string(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    # Ensure at least one item exists so the baseline count is meaningful
    create_random_item(db)
    response_no_search = client.get(
        f"{settings.API_V1_STR}/items/",
        headers=superuser_token_headers,
    )
    response_empty_search = client.get(
        f"{settings.API_V1_STR}/items/",
        headers=superuser_token_headers,
        params={"search": ""},
    )
    assert response_no_search.status_code == 200
    assert response_empty_search.status_code == 200
    content_no_search = response_no_search.json()
    content_empty_search = response_empty_search.json()
    # Both should return the same total count and same number of items in data
    assert content_empty_search["count"] == content_no_search["count"]
    assert len(content_empty_search["data"]) == len(content_no_search["data"])
