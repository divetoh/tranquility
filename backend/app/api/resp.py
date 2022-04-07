""" Dict with standart responses """
from typing import Dict

C34: Dict = {
    403: {"description": "Not enough privileges"},
    404: {"description": "Item not found"},
}

C3: Dict = {
    403: {"description": "Not enough privileges"},
}

C4: Dict = {
    404: {"description": "Item not found"},
}

C9DEL: Dict = {
    409: {"description": "Delete conflict"},
}

C9UID: Dict = {
    409: {"description": "Object identificator not unique"},
}
