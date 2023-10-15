from textual.app import ComposeResult
from textual.containers import Grid
from textual.screen import ModalScreen
from textual.widgets import Button, Label, Footer


class ConfirmDialog(ModalScreen):
    CSS = """
    ConfirmDialog {
        align: center middle;
    }
    
    #dialog {
        grid-size: 2;
        grid-gutter: 1 2;
        grid-rows: 1fr 3;
        padding: 0 1;
        width: 60;
        height: 11;
        border: thick $background 80%;
        background: $surface;
    }
    
    #question {
        column-span: 2;
        height: 1fr;
        width: 1fr;
        content-align: center middle;
    }
    
    Button {
        width: 100%;
    }
    """

    def __init__(self, question, confirm_text="Yes", cancel_text="No"):
        super().__init__()
        self.question = question
        self.confirm_text = confirm_text
        self.cancel_text = cancel_text

    def compose(self) -> ComposeResult:
        with Grid(id="dialog"):
            yield Label(self.question, id="question")
            yield Button(self.confirm_text, variant="primary", id="confirm")
            yield Button(self.cancel_text, variant="error", id="cancel")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "confirm":
            self.dismiss(True)
        else:
            self.dismiss(False)
