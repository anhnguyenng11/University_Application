import sys
from tkinter import ttk


BUTTON_CURSOR = "pointinghand" if sys.platform == "darwin" else "hand2"


COLORS = {
    "primary": "#0066cc",
    "primary_hover": "#00488f",
    "primary_pressed": "#003163",
    "link": "#2997ff",
    "on_primary": "#ffffff",
    "danger": "#ff6961",
    "success": "#30d158",
    "red_hover": "#c62828",
    "red_pressed": "#a51f24",
    "focus": "#0071e3",
    "ink": "#f5f5f7",
    "secondary": "#cccccc",
    "disabled": "#8e8e93",
    # Dark equivalents of the surfaces in DESIGN.md.
    "canvas": "#1d1d1f",
    "parchment": "#1d1d1f",
    "pearl": "#272729",
    "field": "#272729",
    "neutral_hover": "#d1d1d6",
    "neutral_pressed": "#b8b8bd",
    "hairline": "#48484a",
    "black": "#000000",
}


def result_color(value):
    if value == "HD":
        return COLORS["link"]
    if value in ("D", "C", "P", "PASS"):
        return COLORS["success"]
    if value in ("Z", "FAIL"):
        return COLORS["danger"]
    return COLORS["ink"]


def color_result_cell(tree, item, column, value):
    tag = f"result_{value}"
    tree.tag_configure(tag, foreground=result_color(value))
    # Tk 9 cell tags let grades and statuses have different colors in the same row.
    tree.tk.call(tree, "tag", "cell", "add", tag, ((item, column),))


def update_button_cursor(event):
    button = event.widget
    button.configure(cursor="arrow" if button.instate(["disabled"]) else BUTTON_CURSOR)


def setup_styles():
    style = ttk.Style()
    if str(style.lookup("UniApp.PageTitle.TLabel", "font")) == "UniApp.Title":
        return

    style.theme_use("clam")
    style.master.configure(background=COLORS["canvas"])
    families = style.tk.splitlist(style.tk.call("font", "families"))
    family = style.tk.call("font", "actual", "TkDefaultFont", "-family")
    for candidate in ("SF Pro Text", "Helvetica Neue"):
        if candidate in families:
            family = candidate
            break
    display_family = "SF Pro Display" if "SF Pro Display" in families else family

    for name, pixels, weight in (
        ("Body", 17, "normal"),
        ("Caption", 14, "normal"),
        ("CaptionStrong", 14, "bold"),
        ("Strong", 17, "bold"),
        ("Section", 21, "bold"),
        ("Title", 34, "bold"),
        ("AdminTitle", 26, "bold"),
        ("Hero", 40, "bold"),
        ("Metric", 24, "bold"),
    ):
        # Tk uses points; convert the reference's pixel sizes at the current scaling.
        size = style.tk.call("expr", f"round({pixels} / [tk scaling])")
        style.tk.call(
            "font", "create", f"UniApp.{name}",
            "-family", display_family if name in ("Title", "AdminTitle", "Hero") else family,
            "-size", size, "-weight", weight
        )

    style.configure(".", background=COLORS["canvas"], foreground=COLORS["ink"],
                    fieldbackground=COLORS["field"], troughcolor=COLORS["parchment"],
                    bordercolor=COLORS["hairline"], lightcolor=COLORS["canvas"],
                    darkcolor=COLORS["canvas"])
    style.map(".", background=[("disabled", COLORS["parchment"]),
                               ("active", COLORS["canvas"])],
              foreground=[("disabled", COLORS["disabled"])])
    style.configure("TFrame", background=COLORS["canvas"])
    style.configure("TLabel", background=COLORS["canvas"],
                    foreground=COLORS["ink"], font="UniApp.Body")
    style.configure("UniApp.Page.TFrame", background=COLORS["parchment"])
    style.configure("UniApp.Header.TFrame", background=COLORS["black"])
    for name, font, background, foreground in (
        ("Title", "Title", "canvas", "ink"),
        ("Hero", "Hero", "canvas", "ink"),
        ("PageTitle", "Title", "parchment", "ink"),
        ("AdminTitle", "AdminTitle", "parchment", "ink"),
        ("PageText", "Body", "parchment", "secondary"),
        ("PageCaption", "Caption", "parchment", "secondary"),
        ("PageStrong", "Strong", "parchment", "ink"),
        ("PageMetric", "Metric", "parchment", "ink"),
        ("Muted", "Body", "canvas", "secondary"),
        ("Caption", "Caption", "canvas", "secondary"),
        ("Strong", "Strong", "canvas", "ink"),
        ("Metric", "Metric", "canvas", "ink"),
        ("Brand", "Section", "black", "ink"),
        ("Role", "Caption", "black", "ink"),
    ):
        style.configure(f"UniApp.{name}.TLabel", font=f"UniApp.{font}",
                        background=COLORS[background], foreground=COLORS[foreground])

    style.configure("UniApp.Section.TLabelframe", background=COLORS["parchment"],
                    borderwidth=0, relief="flat")
    style.configure("UniApp.Section.TLabelframe.Label", font="UniApp.Section",
                    background=COLORS["parchment"], foreground=COLORS["ink"])
    style.configure("UniApp.Card.TLabelframe", background=COLORS["parchment"],
                    bordercolor=COLORS["hairline"], lightcolor=COLORS["parchment"],
                    darkcolor=COLORS["parchment"], borderwidth=1, relief="solid")
    style.configure("UniApp.Card.TLabelframe.Label", font="UniApp.Strong",
                    background=COLORS["parchment"], foreground=COLORS["ink"])
    style.configure("UniApp.Plain.TLabelframe", background=COLORS["parchment"],
                    borderwidth=0, relief="flat")
    style.configure("Compact.UniApp.Card.TLabelframe.Label", font="UniApp.CaptionStrong")
    style.configure("TSeparator", background=COLORS["hairline"])

    for name, background, foreground, border, hover, pressed in (
        ("Primary", "primary", "on_primary", "primary", "primary_hover", "primary_pressed"),
        ("Secondary", "canvas", "link", "link", "primary_hover", "primary_pressed"),
        ("Utility", "canvas", "secondary", "secondary", "neutral_hover", "neutral_pressed"),
        ("Nav", "parchment", "link", "link", "primary_hover", "primary_pressed"),
        ("Danger", "canvas", "danger", "danger", "red_hover", "red_pressed"),
    ):
        button_style = f"UniApp.{name}.TButton"
        style.configure(button_style, font="UniApp.Body", padding=(22, 11),
                        background=COLORS[background], foreground=COLORS[foreground],
                        bordercolor=COLORS[border], lightcolor=COLORS[background],
                        darkcolor=COLORS[background], borderwidth=0, relief="flat",
                        focusthickness=2,
                        focuscolor=COLORS["on_primary"] if name == "Primary" else COLORS[foreground],
                        anchor="w" if name == "Nav" else "center")
        fill_states = [("disabled", COLORS["parchment"]),
                       ("pressed", COLORS[pressed]),
                       ("active", COLORS[hover])]
        hover_foreground = COLORS["black"] if name == "Utility" else COLORS["on_primary"]
        style.map(button_style,
                  foreground=[("disabled", COLORS["disabled"]),
                              ("pressed", hover_foreground),
                              ("active", hover_foreground)],
                  background=fill_states,
                  bordercolor=[("disabled", COLORS["hairline"]),
                               ("pressed", COLORS[pressed]),
                               ("active", COLORS[hover]),
                               ("focus", COLORS[border])],
                  focuscolor=[("disabled", COLORS["disabled"]),
                              ("pressed", hover_foreground),
                              ("active", hover_foreground)],
                  lightcolor=fill_states,
                  darkcolor=fill_states,
                  relief=[("disabled", "flat"), ("pressed", "flat")])

    style.configure("Sidebar.UniApp.Danger.TButton", anchor="w")

    for name in ("Primary", "Secondary", "Utility", "Danger"):
        style.configure(f"Compact.UniApp.{name}.TButton", font="UniApp.Caption",
                        padding=(14, 7), width=0)

    style.master.bind_class("TButton", "<Enter>", update_button_cursor, add="+")
    style.master.bind_class("TButton", "<Motion>", update_button_cursor, add="+")
    style.master.bind_class("TButton", "<Map>", update_button_cursor, add="+")

    style.configure("UniApp.TEntry", font="UniApp.Body", padding=(12, 10),
                    fieldbackground=COLORS["field"], foreground=COLORS["ink"],
                    bordercolor=COLORS["hairline"], lightcolor=COLORS["field"],
                    darkcolor=COLORS["field"], insertcolor=COLORS["ink"],
                    selectbackground=COLORS["primary"], selectforeground=COLORS["on_primary"])
    style.map("UniApp.TEntry", fieldbackground=[("disabled", COLORS["field"]),
                                                ("readonly", COLORS["field"])],
              foreground=[("disabled", COLORS["disabled"])],
              bordercolor=[("focus", COLORS["focus"])],
              lightcolor=[("focus", COLORS["focus"])],
              darkcolor=[("focus", COLORS["focus"])])
    style.configure("Compact.UniApp.TEntry", padding=(10, 6))

    row_height = style.tk.call("expr", "[font metrics UniApp.Body -linespace] + 8")
    compact_row_height = style.tk.call("expr", "[font metrics UniApp.Caption -linespace] + 6")
    for tree_style, font, height in (
        ("UniApp.Treeview", "UniApp.Body", row_height),
        ("Compact.UniApp.Treeview", "UniApp.Caption", compact_row_height),
        ("AdminStudents.Treeview", "UniApp.Caption", compact_row_height),
    ):
        style.configure(tree_style, font=font, rowheight=height,
                        background=COLORS["field"], fieldbackground=COLORS["field"],
                        foreground=COLORS["ink"], bordercolor=COLORS["hairline"],
                        lightcolor=COLORS["field"], darkcolor=COLORS["field"],
                        borderwidth=1)
        style.configure(f"{tree_style}.Heading", font="UniApp.CaptionStrong", padding=(8, 4),
                        background=COLORS["parchment"], foreground=COLORS["ink"],
                        relief="flat", bordercolor=COLORS["hairline"])
        style.map(tree_style, background=[("selected", COLORS["primary"])],
                  foreground=[("selected", COLORS["on_primary"])])
        style.map(f"{tree_style}.Heading", background=[("active", COLORS["parchment"])])

    for scrollbar in ("Horizontal.TScrollbar", "Vertical.TScrollbar"):
        style.configure(scrollbar, background=COLORS["pearl"],
                        troughcolor=COLORS["parchment"], arrowcolor=COLORS["secondary"],
                        bordercolor=COLORS["hairline"], lightcolor=COLORS["pearl"],
                        darkcolor=COLORS["pearl"])
        style.map(scrollbar, background=[("pressed", COLORS["hairline"]),
                                        ("active", COLORS["pearl"])])


class BaseGUIView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        setup_styles()

    def create_auth_entry(self, parent, text, label_style, show=""):
        ttk.Label(
            parent,
            text=text,
            style=label_style
        ).pack(anchor="w", pady=(0, 8))

        entry = ttk.Entry(
            parent,
            font="UniApp.Body",
            style="UniApp.TEntry",
            show=show
        )
        entry.pack(fill="x", pady=(0, 24))
        return entry
