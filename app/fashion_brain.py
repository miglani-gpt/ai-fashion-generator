 
# IMPORTS
import math

# CONSTANTS
GARMENTS = ["lehenga", "gown", "dress", "kurta", "saree"]

COLORS = [
    "red", "blue", "green", "black", "white",
    "yellow", "pink", "purple", "orange", "brown"
]

FABRICS = [
    "silk", "cotton", "denim", "linen",
    "velvet", "chiffon", "wool"
]

COLOR_MAP = {
    "red": "#ff0000",
    "blue": "#0000ff",
    "green": "#00ff00",
    "black": "#000000",
    "white": "#ffffff",
    "yellow": "#ffff00",
    "pink": "#ffc0cb",
    "purple": "#800080",
    "orange": "#ffa500",
    "brown": "#8b4513",
}


# COLOR HELPERS
def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def hex_to_color_name(hex_color):
    """
    Convert HEX → closest known color name
    """
    target = hex_to_rgb(hex_color)

    closest = None
    min_dist = float("inf")

    for name, hex_val in COLOR_MAP.items():
        rgb = hex_to_rgb(hex_val)
        dist = sum((a - b) ** 2 for a, b in zip(target, rgb))

        if dist < min_dist:
            min_dist = dist
            closest = name

    return closest


# STATE UPDATE
def update_state(state: dict, user_input: str) -> dict:
    user_input = user_input.lower()

    words = user_input.split()

    # detect color from text first
    for c in COLORS:
        if c in user_input:
            state["color"] = c

    # garment
    for g in GARMENTS:
        if g in words:
            state["garment"] = g

    # fabric
    for f in FABRICS:
        if f in words:
            state["fabric"] = f

    # details
    for word in words:
        if word not in GARMENTS + COLORS + FABRICS:
            if word not in state["details"]:
                state["details"].append(word)

    return state


# PROMPT BUILDER
def build_prompt(state: dict, enhance: bool = False) -> str:
    parts = []

    if state["color"]:
        parts.append(state["color"])

    if state["fabric"]:
        parts.append(state["fabric"])

    if state["garment"]:
        parts.append(state["garment"])

    if state["details"]:
        parts.append(" ".join(state["details"]))

    base = ", ".join(parts)

    # enhance 
    if enhance and "high fashion" not in base:
        base += ", high fashion, couture, ultra detailed, professional lighting"

    return base + ", fashion design, haute couture, high resolution"