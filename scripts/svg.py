from xml.sax.saxutils import escape


TEXT = "#c9d1d9"
KEY = "#d19a66"
VALUE = "#a5d6ff"
MUTED = "#7d8590"

def text(x, y, value, *, fill="#c9d1d9", size=20, anchor="start"):
    """Return a single SVG <text> element."""

    return f'''<text
        x="{x}"
        y="{y}"
        text-anchor="{anchor}"
        font-size="{size}"
        fill="{fill}">{escape(str(value))}</text>'''