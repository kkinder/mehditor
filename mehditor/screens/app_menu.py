from collections import OrderedDict

from rich.table import Table
from textual import events, on
from textual.binding import Binding
from textual.containers import Horizontal, Vertical, Container
from textual.screen import ModalScreen
from textual.widgets import Footer, TabbedContent, TabPane, OptionList, Tabs, Label, Button, Static, Markdown, Header
from textual.widgets._tabbed_content import ContentTabs
from textual.widgets.option_list import Separator, Option
from mehditor import config

class AppMenu(ModalScreen):
    CSS = """
    AppMenu {
        align: center middle;
    }
    
    #dialog {
        width: 80%;
        height: 70%;
        border: thick $background 80%;
        background: $panel-darken-1;
        padding: 0
    }
    
    TabbedContent {
        padding: 0;
        height: 100%;
    }
    
    TabPane {
        padding: 0;
        height: 100%;
        background: $panel;
    }
    
    ContentSwitcher {
        padding: 0;
        height: 100%;
        background: $panel;
    }
    
    OptionList {
        border: none;
        background: $panel;
    }
    
    Button {
        border: none;
        height: 1
    }

    #toolstrip {
        align: center bottom;
        height: 1fr;
        
    }
    
    """

    BINDINGS = [
        Binding("f", "show_tab('file')", "File"),
        Binding("e", "show_tab('edit')", "Edit"),
        Binding("w", "show_tab('view')", "View"),
        Binding("h", "show_tab('help')", "Help"),
    ]

    menus = OrderedDict()
    menus["file"] = [
        "f", "File", [
            ["new_file", "New", "n"],
            ["open_file", "Open...", "o"],
            ["save_file", "Save", "s"],
            ["save_file_as", "Save As...", "a"],
            "-",
            ["quit", "Quit", "q"],
            ["suspend_process", "Suspend", "u"]
        ]
    ]
    menus["edit"] = [
        "e", "Edit", [
            ["cut", "Cut", "x"],
            ["copy", "Copy", "c"],
            ["paste", "Paste", "v"],
            ["undo_change", "Undo", "u"],
            ["redo_change", "Redo", "r"],
        ]
    ]
    menus["view"] = [
        "w", "View", [
            ["change_theme", "Theme...", "t"],
            ["toggle_dark_mode", "Toggle Light/Dark Mode", "d"],
            ["toggle_line_numbers", "Toggle Line Numbers", "l"],
            "-",
            ["change_file_type", "File type...", "y"],
            ["toggle_soft_wrap", "Toggle soft wrap...", "s"],

            # This seems to be broken up stream
            ["set_indent_type", "Set Indent Type...", "n"],
            ["set_indent_width", "Set Indent Width...", "i"],
        ]
    ]
    menus["help"] = [
        "h", "Help", [
            ["show_shortcuts", "Show Showcuts", "s"],
            ["show_about", "About...", "a"],
        ]
    ]

    def compose(self):
        self.menu_hotkeys = []
        self.menu_hotkey_items = {}
        for menu_id, menu_data in self.menus.items():
            hotkey, label, items = menu_data
            self.menu_hotkeys.append(hotkey)
            self.menu_hotkey_items[menu_id] = {}
            for item in items:
                if item != "-":
                    self.menu_hotkey_items[menu_id][item[2]] = item[0]

        with Container(id="dialog"):
            with TabbedContent(id="tabber", initial=f"{next(iter(self.menus.keys()))}"):
                for menu_id, menu_data in self.menus.items():
                    hotkey, label, items = menu_data

                    with TabPane(f"{hotkey}: {label}", id=f"{menu_id}"):
                        options = []
                        for item in items:
                            if item == "-":
                                options.append(Separator())
                                continue
                            elif len(item) == 3:
                                command, item_label, item_hotkey = item
                            else:
                                raise ValueError(f"Invalid menu item: {item}")

                            if config.settings.has_option('shortcuts', command):
                                item_binding = config.settings.get('shortcuts', command)
                            else:
                                item_binding = None

                            if item_hotkey and item_hotkey in self.menu_hotkeys:
                                raise Exception(f"Hotkey {item_hotkey} already in use by menu")

                            table = Table.grid(padding=0, pad_edge=False, expand=True)
                            table.add_column()
                            table.add_column(justify="right")

                            if item_binding:
                                table.add_row(f"[bold]{item_hotkey}:[/] {item_label}", f'[yellow]{item_binding}[/]')
                            else:
                                table.add_row(f"[bold]{item_hotkey}:[/] {item_label}", "")

                            options.append(Option(table, id=f"option-{command}"))

                        yield OptionList(
                            *options,
                            id=f"{menu_id}-list")

            yield Footer()

    def _on_mount(self, event: events.Mount) -> None:
        super()._on_mount(event)
        self.query_one(f"#{self.query_one(TabbedContent).active}-list").focus()

    def action_show_tab(self, tab: str) -> None:
        self.tabs.active = tab
        self.query_one(f"#{tab}-list").focus()

    @on(TabbedContent.TabActivated)
    def on_tab_pane_tab_activated(self, event) -> None:
        self.query_one(f"#{event.pane.id}-list").focus()

    def on_key(self, event: events.Key) -> None:
        if event.key == "left":
            self.query_one("#tabber").get_child_by_type(ContentTabs).action_previous_tab()
        elif event.key == "right":
            self.query_one("#tabber").get_child_by_type(ContentTabs).action_next_tab()
        elif event.key in self.menu_hotkeys:
            pass
        else:
            current_menu_keys = self.menu_hotkey_items[self.tabs.active]
            if event.key in current_menu_keys:
                self.dismiss(current_menu_keys[event.key])

    def on_option_list_option_selected(self, event):
        self.dismiss(event.option.id.split('-', 1)[1])

    @property
    def tabs(self):
        return self.query_one("#tabber")
