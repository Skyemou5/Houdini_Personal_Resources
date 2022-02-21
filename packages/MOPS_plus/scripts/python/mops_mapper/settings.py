import os

ATTR_TYPES = [
"int",
"float",
"vector3",
"string",
"color",
]

ATTR_SECTION_HEIGHT = 10

COLORS = {
    "bg": {
        "idle": "#2e2e2e",
        "selected": "#57482a",
    },
}

ICONS = {
    "op_chooser": os.path.join(os.path.dirname(__file__), 'op_chooser.jpg'),
    "file_chooser": os.path.join(os.path.dirname(__file__), 'file_chooser.jpg'),
}