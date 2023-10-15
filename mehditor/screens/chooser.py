from textual import on
from textual.app import ComposeResult
from textual.containers import Vertical, Container
from textual.screen import ModalScreen
from textual.widgets import Label, ListView, ListItem


class Chooser(ModalScreen):
    CSS = """
    Chooser {
        align: center middle;
    }

    #dialog {
        max-width: 60;
        max-height: 20;
        border: thick $background 80%;
        background: $surface;
    }
    
    #question {
        height: 3;
    }
    
    ListView {
    }
    
    Label {
        padding: 1 2;
    }
    """

    def __init__(self, question, choices, default=None):
        super().__init__()
        self.question = question
        self.choices = choices

        self.initial_index = 0
        if default:
            for i, item in enumerate(self.choices):
                if item[0] == default:
                    self.initial_index = i


    def compose(self) -> ComposeResult:
        with Vertical(id="dialog"):
            yield Container(Label(self.question), id="question")
            yield ListView(*[ListItem(Label(label), id=i, classes="choices") for i, label in self.choices],
                           id="choices", classes="choices", initial_index=self.initial_index)

    @on(ListView.Selected)
    def selected(self, event):
        self.dismiss(event.item.id)
