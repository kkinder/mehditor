import functools
from pathlib import Path

from textual import on
from textual.app import App, ComposeResult
from textual.notifications import Notification
from textual.reactive import reactive
from textual.screen import ModalScreen
from textual.widgets import Header, Input, Footer
from textual.widgets._text_area import ThemeDoesNotExist

from mehditor import config
from mehditor.app_commands import AppCommands
from mehditor.screens.about import About
from mehditor.screens.app_menu import AppMenu
from mehditor.screens.chooser import Chooser
from mehditor.screens.confirm_dialog import ConfirmDialog
from mehditor.screens.file_open import FileOpen
from mehditor.screens.file_save import FileSave
from mehditor.screens.input_prompt import InputPrompt
from mehditor.screens.quit_screen import QuitScreen
from mehditor.screens.shortcuts import Shortcuts
from mehditor.validators import LineNumber
from mehditor.widgets.better_text_area import BetterTextArea

known_dark_themes = {
    "monokai",
    "dracula",
    "vscode_dark",
}

known_light_themes = {
    "github_light"
}


def handle_os_error_decorator(error_message, severity="error", timeout=Notification.timeout):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except OSError as e:
                self.notify(title=error_message, message=str(e), severity=severity, timeout=timeout)

        return wrapper

    return decorator


class MeheditorApp(App):
    BINDINGS = [
        config.generate_binding("menu"),
        config.generate_binding("quit"),
        config.generate_binding("save_file"),
        config.generate_binding("new_file"),
        config.generate_binding("goto_line"),
        config.generate_binding("suspend_process"),
    ]

    COMMANDS = {AppCommands}

    DEFAULT_CSS = """
    .hidden {
        display: none;
    }
    #text-buffer {
        border: none;
    }
    """

    show_line_numbers = reactive(True)
    soft_wrap = reactive(False)
    indent_type = reactive("spaces")
    indent_width = reactive(4)
    theme = reactive("default")
    file_type = reactive("text")
    show_line_finder = reactive(False)
    file = reactive(Path)
    file_unsaved = reactive(False)
    clipboard = reactive('')

    def __init__(self, file):
        super().__init__()
        self.initial_file = file

    def on_mount(self):
        self.indent_type = config.settings['editing']['indent_type']
        self.indent_width = config.settings.getint('editing', 'indent_width')

        try:
            self.theme = config.settings['editing']['theme']
        except ThemeDoesNotExist:
            self.notify(f"Configured theme not available: {config.settings['editing']['theme']}", severity="error")
        self.dark = config.settings.getboolean('editing', 'dark_mode')
        self.show_line_numbers = config.settings.getboolean('editing', 'show_line_numbers')
        self.soft_wrap = config.settings.getboolean('editing', 'soft_wrap')

        if self.initial_file:
            self.open_file(self.initial_file)
        else:
            self.new_file()
        self.query_one("#text-buffer").focus()

    #################################################################
    ## Internal actions to be used elsewhere                       ##
    #################################################################
    def new_file(self):
        self.query_one("#text-buffer").load_text("")
        self.query_one("#text-buffer").history.clear()
        self.file = None
        self.title = '(Untitled)'
        self.file_unsaved = False

    @handle_os_error_decorator("Error Opening File")
    def open_file(self, file):
        file = Path(file)
        if file.exists():
            try:
                text = file.read_text()
            except UnicodeDecodeError as e:
                self.notify(f'Error decoding file (is it a text file?): {e}', severity="error", timeout=20)
                return
        else:
            text = ''

        self.query_one("#text-buffer").load_text(text)
        self.query_one("#text-buffer").history.clear()
        self.file = Path(file).resolve() if file else None
        self.title = self.file.name
        self.file_unsaved = False

    @handle_os_error_decorator("Error Saving Settings")
    def save_settings(self):
        config.settings['editing']['indent_type'] = self.indent_type
        config.settings['editing']['indent_width'] = str(self.indent_width)
        config.settings['editing']['theme'] = self.theme
        config.settings['editing']['dark_mode'] = 'Yes' if self.dark else 'No'
        config.settings['editing']['show_line_numbers'] = 'Yes' if self.show_line_numbers else 'No'
        config.settings['editing']['soft_wrap'] = 'Yes' if self.soft_wrap else 'No'
        config.save()

    #################################################################
    ## Watchers                                                    ##
    #################################################################
    def watch_theme(self, theme):
        self.query_one("#text-buffer").theme = theme if theme not in (None, "default") else "css"

    def watch_dark(self, *args):
        super().watch_dark(*args)
        if self.dark and self.query_one("#text-buffer").theme in known_light_themes:
            self.notify("Dark mode enabled, but using light theme (try changing editor theme too)")
        elif not self.dark and self.query_one("#text-buffer").theme in known_dark_themes:
            self.notify("Light mode enabled, but using dark theme (try changing editor theme too)")

    def watch_indent_type(self):
        self.query_one("#text-buffer").indent_type = self.indent_type

    def watch_indent_width(self):
        self.query_one("#text-buffer").indent_width = self.indent_width

    def watch_show_line_numbers(self):
        self.query_one("#text-buffer").show_line_numbers = self.show_line_numbers

    def watch_soft_wrap(self):
        self.query_one("#text-buffer").soft_wrap = self.soft_wrap

    def watch_file_type(self):
        if self.file_type == "text":
            self.query_one("#text-buffer").language = None
            self.sub_title = ''
        else:
            self.query_one("#text-buffer").language = self.file_type
            self.sub_title = self.file_type

    def watch_file(self):
        if self.file and '.' in self.file.name:
            extension = self.file.name.split('.')[-1].lower().strip()
            if extension in config.settings['filetypes']:
                self.file_type = config.settings['filetypes'][extension]

    def watch_show_line_finder(self):
        w = self.query_one("#line_number")

        if self.show_line_finder:
            w.remove_class("hidden")
            line, col = self.query_one("#text-buffer").cursor_location
            if col > 0:
                w.value = f"{line + 1}:{col + 1}"
            else:
                w.value = f"{line + 1}"
            w.focus()
        else:
            w.add_class("hidden")

    #################################################################
    ## Main methods and actions                                    ##
    #################################################################
    def compose(self) -> ComposeResult:
        yield Header()

        yield BetterTextArea("", language=None, id="text-buffer", tab_behavior="indent")
        yield Input(
            id="line_number",
            placeholder="Go to line number (eg 10:3 for line 10, col 3)",
            validate_on=["changed"],
            validators=[LineNumber()])
        yield Footer()

    def action_cut(self):
        tb: BetterTextArea = self.query_one("#text-buffer")
        self.clipboard = tb.selected_text
        tb.replace("", tb.selection.start, tb.selection.end)

    def action_copy(self):
        tb: BetterTextArea = self.query_one("#text-buffer")
        if tb.selected_text:
            self.clipboard = tb.selected_text

    def action_paste(self):
        if self.clipboard:
            tb: BetterTextArea = self.query_one("#text-buffer")
            tb.replace(self.clipboard, tb.selection.start, tb.selection.end)
        else:
            self.notify("Nothing to paste", severity="error")

    @handle_os_error_decorator("Error Saving File")
    def action_save_file(self) -> None:

        if self.file:
            self.file.write_text(self.query_one("#text-buffer").text)
            self.file_unsaved = False
            self.notify("File saved")
        else:
            self.action_save_file_as()

    def action_goto_line(self):
        self.show_line_finder = True

    def action_undo_change(self):
        self.query_one("#text-buffer").undo()

    def action_redo_change(self):
        self.query_one("#text-buffer").redo()

    def action_menu(self):
        if self.show_line_finder:
            self.show_line_finder = False
            return

        # TODO: Figure out how to do this without checking a private attribute
        if len(self._screen_stack) == 1:
            def menu_action(action):
                if hasattr(self, f"action_{action}"):
                    getattr(self, f"action_{action}")()
                else:
                    self.notify(f"Unknown action: {action}", severity="error")

            self.push_screen(AppMenu(), menu_action)
        elif len(self._screen_stack) > 1 and isinstance(self._screen_stack[-1], (ModalScreen)):
            self.pop_screen()

    def action_new_file(self):
        if self.file_unsaved:
            def confirmed(confirm: bool) -> None:
                if confirm:
                    self.new_file()

            self.push_screen(ConfirmDialog("File not saved. Erase and start new file?"), confirmed)
        else:
            self.new_file()

    def action_open_file(self):
        def check_result(file):
            self.open_file(file)

        self.push_screen(FileOpen(self.file), check_result)

    def action_save_file_as(self):
        def check_result(file):
            self.file = file
            self.title = self.file.name
            self.action_save_file()

        self.push_screen(FileSave(self.file), check_result)

    def action_show_about(self):
        self.push_screen(About())

    def action_show_shortcuts(self):
        self.push_screen(Shortcuts())

    def action_change_file_type(self):
        def check_result(result):
            self.file_type = result

        self.push_screen(
            Chooser(
                "Choose File Type",
                [("text", "text")] + [(l, l) for l in self.query_one("#text-buffer").available_languages],
                default=self.file_type
            ),
            check_result)

    def action_set_indent_type(self):
        def check_result(result):
            self.indent_type = result
            self.save_settings()

        self.push_screen(
            Chooser(
                "Choose indentation type",
                [("tabs", "Tabs"), ("spaces", "Spaces")],
                default=self.indent_type
            ),
            check_result)

    def action_toggle_dark_mode(self):
        self.dark = not self.dark
        self.save_settings()

    def action_toggle_line_numbers(self):
        self.show_line_numbers = not self.show_line_numbers
        self.save_settings()

    def action_toggle_soft_wrap(self):
        self.soft_wrap = not self.soft_wrap
        self.save_settings()

    def action_set_indent_width(self):
        def check_result(result):
            try:
                self.indent_width = int(result)
            except ValueError:
                self.notify(f"Invalid number: {result}", severity="error")
            self.save_settings()

        self.push_screen(
            InputPrompt(
                "Choose indentation level",
                str(self.indent_width)
            ),
            check_result)

    def action_change_theme(self):
        def check_result(result):
            self.theme = result
            self.save_settings()

        self.push_screen(
            Chooser(
                "Choose Theme",
                [(l, l) for l in self.query_one("#text-buffer").available_themes],
                default=self.theme
            ),
            check_result)

    def action_quit(self) -> None:
        if not self.file_unsaved:
            return self.exit()

        if len(self._screen_stack) > 1 and isinstance(self._screen_stack[-1], QuitScreen):
            self.exit()

        def check_quit(result):
            if result == "save-and-quit":
                if self.file:
                    self.file.write_text(self.query_one("#text-buffer").text)
                    self.exit()
                else:
                    def check_result(file):
                        self.file = file
                        self.title = self.file.name
                        self.action_save_file()
                        self.exit()

                    self.push_screen(FileSave(self.file), check_result)
            elif result == "quit-without-save":
                self.exit()
            elif result == "cancel":
                pass
            elif result == "suspend":
                self.action_suspend_process()
            else:
                self.notify(f"Unknown result: {result}", severity="error")

        self.push_screen(QuitScreen(), check_quit)

    #################################################################
    ## Events                                                      ##
    #################################################################
    @on(Input.Submitted, "#line_number")
    def on_line_number_submitted(self, event):
        linenumber = event.value
        if LineNumber().validate(linenumber).is_valid:
            if ':' in linenumber:
                line, col = linenumber.split(':', 1)
                line = int(line) - 1
                col = int(col) - 1
            else:
                line = int(linenumber) - 1
                col = 0
            self.query_one("#text-buffer").move_cursor((line, col))
            self.show_line_finder = False
            self.query_one("#text-buffer").focus()
        else:
            self.notify(f'Not a valid line number', severity="error")

    @on(BetterTextArea.Changed, "#text-buffer")
    def on_text_buffer_changed(self, event):
        self.file_unsaved = True
