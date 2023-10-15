from textual import on
from textual.app import ComposeResult
from textual.containers import Vertical, Container
from textual.screen import ModalScreen
from textual.widgets import Label, Input, Button


class InputPrompt(ModalScreen):
    CSS = """
    InputPrompt {
        align: center middle;
    }

    #dialog {
        max-width: 60;
        height: 12;
        border: thick $background 80%;
        background: $surface;
    }

    #question {
        height: 3;
        padding: 0 2
    }
    
    Button {
        margin: 1 0 0 0;
        width: 100%
    }
    """

    def __init__(self, question, value):
        super().__init__()
        self.question = question
        self.value = value

    def compose(self) -> ComposeResult:
        with Vertical(id="dialog"):
            yield Container(Label(self.question), id="question")
            yield Input(value=str(self.value), id="input")
            yield Button("OK", id="ok", variant="primary")

    @on(Input.Submitted)
    @on(Button.Pressed)
    def selected(self, event):
        self.dismiss(self.query_one("#input").value)
