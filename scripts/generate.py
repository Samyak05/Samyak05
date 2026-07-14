from pathlib import Path

from scripts.renderer import (
    build_identity,
    build_system,
    build_languages,
    build_tools,
)

TEMPLATE = Path("assets/template.svg")
OUTPUT = Path("assets/terminal.svg")


def main():
    svg = TEMPLATE.read_text(encoding="utf-8")

    svg = svg.replace(
        "{{identity}}",
        build_identity()
    )

    svg = svg.replace(
        "{{system}}",
        build_system()
    )

    svg = svg.replace(
        "{{languages}}",
        build_languages()
    )

    svg = svg.replace(
        "{{tools}}",
        build_tools()
    )

    OUTPUT.write_text(svg, encoding="utf-8")

    print("Generated terminal.svg")


if __name__ == "__main__":
    main()