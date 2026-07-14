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

def line(x1, y1, x2, y2, color="#c9d1d9", width=2):
    return f'''
    <line
        x1="{x1}"
        y1="{y1}"
        x2="{x2}"
        y2="{y2}"
        stroke="{color}"
        stroke-width="{width}"/>
    '''

def rich_text(x, y, parts, size=20):
    """
    parts = [
        ("text", "#color"),
        ("another", "#color"),
    ]
    """

    svg = f'<text x="{x}" y="{y}" font-size="{size}">'

    for value, color in parts:
        svg += f'<tspan fill="{color}">{value}</tspan>'

    svg += "</text>"

    return svg