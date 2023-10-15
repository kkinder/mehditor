from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, MarkdownViewer

ABOUT = """
# Mehditor
Version {version}

A text editor for twentieth century computing. Built with Python and Textual.

© Copyright 2023 Ken Kinder {email} {site}

""".format(
    version="0.1.1",
    author="Ken Kinder",
    email="ken@kkinder.com",
    site="kkinder.com"
)


class About(ModalScreen):
    CSS = """
    About {
        align: center middle;
    }

    #dialog {
        max-width: 70;
        max-height: 18;
        border: thick $background 80%;
        background: $surface;
    }

    Button {
        width: 100%;
    }
    
    MarkdownViewer {
        height: 1fr;
    }
    """

    def compose(self) -> ComposeResult:
        with Vertical(id="dialog"):
            yield MarkdownViewer(ABOUT, show_table_of_contents=False)
            yield Button("Dismiss", variant="primary")

    def on_mount(self):
        self.query_one("Button").focus()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.dismiss()
