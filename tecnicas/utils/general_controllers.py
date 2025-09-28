def getId(value: object | int) -> int | None:
    if isinstance(value, int):
        return value
    elif hasattr(value, "id"):
        return value.id
    elif hasattr(value, "pk"):
        return value.pk

    return None
