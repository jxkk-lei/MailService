def create_mailing_list(
    list_id: int,
    name: str,
    owner_id: int
) -> dict:
    return {
        "id": list_id,
        "name": name,
        "owner_id": owner_id,
    }