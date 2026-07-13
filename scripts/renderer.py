from config.profile import PROFILE
from scripts.svg import text


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
        text(
            470,
            170,
            "-" * len(username),
            fill="#c9d1d9"
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

        line = f"{key}:{dots} {value}"

        parts.append(
            text(
                470,
                y,
                line,
                fill="#c9d1d9"
            )
        )

        y += 30

    return "\n".join(parts)