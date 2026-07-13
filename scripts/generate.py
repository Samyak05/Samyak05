from pathlib import Path

TEMPLATE = Path("assets/template.svg")
OUTPUT = Path("assets/terminal.svg")


def main():

    svg = TEMPLATE.read_text(encoding="utf-8")

    OUTPUT.write_text(svg, encoding="utf-8")

    print("Generated terminal.svg")


if __name__ == "__main__":
    main()