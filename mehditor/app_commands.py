from textual.command import Hit, Hits, Provider
from mehditor.screens.app_menu import AppMenu

command_help = {
    "new_file": "Create new empty file, replacing current one",
    "open_file": "Open new or existing file by name",
    "save_file": "Save current file",
    "save_file_as": "Save current file with new name",
    "quit": "Exit application",
    "suspend_process": "Suspend Process",
    "cut": "Cut selected text to clipboard",
    "copy": "Copy selected text to clipboard",
    "paste": "Paste text from clipboard",
    "undo_change": "Undo last modification",
    "redo_change": "Redo last undo operation",
    "change_theme": "Change editor theme (separate from application light/dark mode)",
    "toggle_dark_mode": "Toggle application light/dark mode (separate from editor theme)",
    "toggle_line_numbers": "Toggle line number visibility",
    "toggle_soft_wrap": "Toggle soft wrap",
    "change_file_type": "Change current file type (language and syntax highlighting)",
    "set_indent_type": "Switch between using tabs and spaces",
    "set_indent_width": "Choose width of tabs or number of spaces to align when pressing tab key",
    "show_shortcuts": "Show keyboard shortcuts",
    "show_about": "About this application"
}


class AppCommands(Provider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.commands = []

        for menu_id, menu_data in AppMenu.menus.items():
            hotkey, label, items = menu_data
            for item in items:
                if item == "-":
                    continue
                elif len(item) == 3:
                    command, item_label, item_hotkey = item
                elif len(item) == 4:
                    command, item_label, item_hotkey, item_binding = item
                else:
                    raise ValueError(f"Invalid menu item: {item}")
                self.commands.append((
                    item_label,
                    getattr(self.app, f"action_{command}"),
                    command_help.get(command, None)
                ))

    async def search(self, query: str) -> Hits:
        matcher = self.matcher(query)

        for name, runnable, help_text in self.commands:
            match = matcher.match(f"{name} {help_text}" if help_text else name)
            if match > 0:
                yield Hit(
                    match,
                    matcher.highlight(name),
                    runnable,
                    help=help_text,
                )
