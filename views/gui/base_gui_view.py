from tkinter import ttk


COLORS = {
    "primary": "#0066cc",
    "primary_pressed": "#0052a3",
    "blue_hover": "#e8f1fb",
    "blue_pressed": "#d2e5f9",
    "danger": "#c62828",
    "red_hover": "#fff1f0",
    "red_pressed": "#ffe0dd",
    "focus": "#0071e3",
    "ink": "#1d1d1f",
    "secondary": "#333333",
    "disabled": "#7a7a7a",
    "canvas": "#ffffff",
    "parchment": "#f5f5f7",
    "pearl": "#fafafc",
    "neutral_hover": "#ededf0",
    "hairline": "#e0e0e0",
    "black": "#000000",
}


def update_button_cursor(event):
    event.widget.configure(cursor="" if event.widget.instate(["disabled"]) else "hand2")


def setup_styles():
    style = ttk.Style()
    if style.lookup("UniApp.Page.TFrame", "background") == COLORS["parchment"]:
        return

    style.theme_use("clam")
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
        ("Brand", "Section", "black", "canvas"),
        ("Role", "Caption", "black", "canvas"),
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
        ("Primary", "primary", "canvas", "primary", "focus", "primary_pressed"),
        ("Secondary", "canvas", "primary", "primary", "blue_hover", "blue_pressed"),
        ("Utility", "pearl", "secondary", "secondary", "neutral_hover", "hairline"),
        ("Nav", "parchment", "primary", "primary", "blue_hover", "blue_pressed"),
        ("Danger", "canvas", "danger", "danger", "red_hover", "red_pressed"),
    ):
        button_style = f"UniApp.{name}.TButton"
        style.configure(button_style, font="UniApp.Body", padding=(22, 11),
                        background=COLORS[background], foreground=COLORS[foreground],
                        bordercolor=COLORS[border], lightcolor=COLORS[background],
                        darkcolor=COLORS[background], borderwidth=1, relief="solid",
                        focusthickness=2,
                        focuscolor=COLORS["canvas"] if name == "Primary" else COLORS[foreground],
                        anchor="w" if name == "Nav" else "center")
        fill_states = [("disabled", COLORS["parchment"]),
                       ("pressed", COLORS[pressed]),
                       ("active", COLORS[hover])]
        style.map(button_style,
                  foreground=[("disabled", COLORS["disabled"])],
                  background=fill_states,
                  bordercolor=[("disabled", COLORS["hairline"]),
                               ("focus", COLORS[border])],
                  lightcolor=fill_states,
                  darkcolor=fill_states,
                  relief=[("disabled", "flat"), ("pressed", "sunken")])

    for name in ("Primary", "Secondary", "Utility", "Danger"):
        style.configure(f"Compact.UniApp.{name}.TButton", font="UniApp.Caption",
                        padding=(14, 7), width=0)

    style.master.bind_class("TButton", "<Enter>", update_button_cursor, add="+")
    style.master.bind_class("TButton", "<Motion>", update_button_cursor, add="+")

    style.configure("UniApp.TEntry", font="UniApp.Body", padding=(12, 10),
                    fieldbackground=COLORS["canvas"], foreground=COLORS["ink"],
                    bordercolor=COLORS["hairline"], lightcolor=COLORS["canvas"],
                    darkcolor=COLORS["canvas"], insertcolor=COLORS["ink"])
    style.map("UniApp.TEntry", bordercolor=[("focus", COLORS["focus"])],
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
                        background=COLORS["canvas"], fieldbackground=COLORS["canvas"],
                        foreground=COLORS["ink"], bordercolor=COLORS["hairline"],
                        lightcolor=COLORS["canvas"], darkcolor=COLORS["canvas"],
                        borderwidth=1)
        style.configure(f"{tree_style}.Heading", font="UniApp.CaptionStrong", padding=(8, 4),
                        background=COLORS["parchment"], foreground=COLORS["ink"],
                        relief="flat", bordercolor=COLORS["hairline"])
        style.map(tree_style, background=[("selected", COLORS["primary"])],
                  foreground=[("selected", COLORS["canvas"])])
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
