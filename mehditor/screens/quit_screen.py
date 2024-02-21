from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Grid, Vertical, Container
from textual.screen import ModalScreen
from textual.widgets import Label, Button


class QuitScreen(ModalScreen):
    BINDINGS = [
        Binding("s", "save_and_quit", "Save and quit", show=False),
        Binding("q", "quit_without_save", "Quit without saving", show=False),
        Binding("c", "cancel", "Cancel", show=False),
        Binding("u", "suspend", "Suspend", show=False),
    ]

    CSS = """
    QuitScreen {
        align: center middle;
    }
    
    #dialog {
        width: 50;
        height: 22;
        border: thick $background 80%;
        background: $surface;
    }
    
    #question {
        align: center middle;
        height: 4;
        width: 100%;
    }
    
    Button {
        width: 100%;
        margin: 1
    }
    """

    def compose(self) -> ComposeResult:
        with Vertical(id="dialog"):
            yield Container(Label("Save file before quitting?"), id="question")
            yield Button("S: Save and quit", id="save-and-quit")
            yield Button("Q: Quit without saving", variant="error", id="quit-without-save")
            yield Button("C: Cancel", id="cancel")
            yield Button("U: Suspend", id="suspend")

    def action_save_and_quit(self) -> None:
        self.dismiss("save-and-quit")

    def action_quit_without_save(self) -> None:
        self.dismiss("quit-without-save")

    def action_cancel(self) -> None:
        self.dismiss("cancel")

    def action_suspend(self) -> None:
        self.dismiss("suspend")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.dismiss(event.button.id)
