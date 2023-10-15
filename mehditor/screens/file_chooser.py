from pathlib import Path

from textual import on
from textual.containers import Vertical, Horizontal
from textual.reactive import reactive
from textual.screen import ModalScreen
from textual.widgets import Button, DirectoryTree, Label
from textual.widgets import Input

from mehditor.screens.confirm_dialog import ConfirmDialog


class FileChooser(ModalScreen):
    CSS = """
    FileChooser { 
        align: center middle;
    }

    #dialog {
        padding: 0;
        width: 85%;
        height: 80%;
        border: thick $background 80%;
        background: $surface;
    }

    #title {
        content-align: center middle;
        width: 100%;
        display: block;
    }

    #nav-area {
        height: 3;
        # background: $primary-background;
    }

    #file-input {
        width: 1fr
    }
    
    Button  {
        margin: 0 1 0 0;
        padding: 0 1;
        min-width: 2;
        width: auto;
    }
    """

    cwd = reactive(str)

    def __init__(self, current_file, confirm_overwrite=False):
        super().__init__()

        if current_file:
            self.current_file = current_file.resolve()
        else:
            self.current_file = None
        self.confirm_overwrite = confirm_overwrite

    def on_mount(self):
        if self.current_file:
            self.cwd = self.current_file.parent
            self.set_input_value(self.current_file.parent)
            self.query_one("#dir-tree").path = self.current_file.parent
        else:
            self.cwd = Path.cwd().resolve()
            self.set_input_value(self.cwd)
            self.query_one("#dir-tree").path = self.cwd
        self.query_one("#file-input").focus()

    def watch_cwd(self):
        self.query_one("#dir-tree").path = self.cwd
        self.set_input_value(self.cwd)

    def set_input_value(self, value):
        value = Path(value)
        if value.is_dir():
            value = f'{value}/'
        else:
            value = str(value)
        self.query_one("#file-input").value = value
        self.query_one("#file-input").action_end()
        self.query_one("#file-input").focus()

    def compose(self):
        with Vertical(id="dialog"):
            yield Label("Choose File", id="title")
            with Horizontal(id="nav-area"):
                yield Button("../", id="up-dir")
                yield Button("/", id="root-dir")
                yield Button("~", id="home-dir")
                yield Input(id="file-input")
            yield DirectoryTree(id="dir-tree", path=Path.cwd().resolve())

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "up-dir":
            self.cwd = self.cwd.parent
        elif event.button.id == "root-dir":
            self.cwd = Path("/")
        elif event.button.id == "home-dir":
            self.cwd = Path.home()
        else:
            self.dismiss(False)

    @on(Input.Submitted, "#file-input")
    def on_file_input_submitted(self, event):
        loc = Path(event.value).resolve()
        if loc.is_file():
            self.choose_file(loc)
        elif loc.is_dir():
            self.cwd = Path(event.value).resolve()
        elif loc.parent.exists():
            # Parent file exists; this is the return value
            self.dismiss(loc)
        else:
            self.notify(f"Invalid path: {loc}", severity="error")

    @on(DirectoryTree.FileSelected)
    def on_file_selected(self, event):
        self.choose_file(event.path)

    def choose_file(self, loc):
        if self.confirm_overwrite and loc.resolve() != self.current_file:
            def confirmed(confirm: bool) -> None:
                if confirm:
                    self.dismiss(loc)

            self.app.push_screen(ConfirmDialog("File already exists. Overwrite?"), confirmed)
        else:
            self.dismiss(loc)
