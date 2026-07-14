from config.profile import PROFILE
from scripts.svg import text, line, rich_text


def build_identity():
    identity = PROFILE["identity"]

    username = identity["username"]
    tagline = identity["tagline"]
    focus = identity["focus"]

    parts = []

    # Username
    parts.append(
        text(
            470,
            150,
            username,
            size=24
        )
    )

    # Underline
    parts.append(
        line(
            470,
            165,
            650,
            165
        )
    )

    # Tagline
    parts.append(
        text(
            470,
            205,
            tagline
        )
    )

    # Focus
    parts.append(
        text(
            470,
            235,
            focus,
            fill="#7d8590"
        )
    )

    return "\n".join(parts)

def build_system():
    system = PROFILE["system"]

    parts = []

    y = 290

    for key, value in system:
        dots = "." * max(1, 25 - len(key))

        parts.append(
            rich_text(
                470,
                y,
                [
                    (f"{key}:", "#d19a66"),
                    (dots, "#7d8590"),
                    (f" {value}", "#a5d6ff"),
                ]
            )
        )

        y += 30

    return "\n".join(parts)

def build_languages():
    languages = PROFILE["languages"]

    parts = []

    y = 450

    for category, value in languages:

        dots = "." * max(1, 16 - len(category))

        parts.append(
            rich_text(
                470,
                y,
                [
                    ("Languages.", "#d19a66"),
                    (category, "#d19a66"),
                    (":" + dots, "#7d8590"),
                    (" " + value, "#a5d6ff"),
                ],
            )
        )

        y += 30

    return "\n".join(parts)

def build_tools():
    tools = PROFILE["tools"]

    parts = []

    y = 540

    for category, value in tools:

        dots = "." * max(1, 18 - len(category))

        parts.append(
            rich_text(
                470,
                y,
                [
                    ("Tools.", "#d19a66"),
                    (category, "#d19a66"),
                    (":" + dots, "#7d8590"),
                    (" " + value, "#a5d6ff"),
                ],
            )
        )

        y += 30

    return "\n".join(parts)

