import webbrowser
from pathlib import Path

from textual import on
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, MarkdownViewer, Markdown
from importlib.metadata import version

ABOUT = """
# Mehditor
Version {version}

A text editor for twentieth century computing. Built with Python and Textual.

https://github.com/kkinder/mehditor

© Copyright 2023-2024 Ken Kinder {email} {site}
""".format(
    version=version("mehditor"),
    author="Ken Kinder",
    email="ken@kkinder.com",
    site="kkinder.com"
)


class MarkdownViewerWithLinks(MarkdownViewer):
    @on(Markdown.LinkClicked)
    def handle_link(self, event: Markdown.LinkClicked) -> None:
        if not Path(event.href).exists():
            event.prevent_default()
            webbrowser.open(event.href)
            # self.notify(f'WTF: {event.href}')


class About(ModalScreen):
    CSS = """
    About {
        align: center middle;
    }

    #dialog {
        max-width: 70;
        max-height: 20;
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
            yield MarkdownViewerWithLinks(ABOUT, show_table_of_contents=False)
            yield Button("Dismiss", variant="primary")

    def on_mount(self):
        self.query_one("Button").focus()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.dismiss()
