""" Dict with standart responses """

C34: dict = {
    403: {"description": "Not enough privileges"},
    404: {"description": "Item not found"},
}

C3: dict = {
    403: {"description": "Not enough privileges"},
}

C4: dict = {
    404: {"description": "Item not found"},
}

C9DEL: dict = {
    409: {"description": "Delete conflict"},
}

C9UID: dict = {
    409: {"description": "Object identificator not unique"},
}
