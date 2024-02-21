from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.screen import ModalScreen
from textual.scroll_view import ScrollView
from textual.widgets import MarkdownViewer

from mehditor import config

SHORTCUTS = """
| Action | Shortcut |
| ------ | -------- |
| Menu | {menu} |
| Command Palette | ctrl+\ |
| Open File | {open_file} |
| Show Shortcuts | {show_shortcuts} |
| Quit | {quit} |
| Suspend | {suspend_process} |
| |
| New File | {new_file} |
| Open File | {open_file} |
| Save File | {save_file} |
| |
| Go to Line | {goto_line} |
| Cut | {cut} |
| Copy | {copy} |
| Paste | {paste} |
| Undo | {undo_change} |
| Redo | {redo_change} |
| |
| Move | ⬆️ ⬇️ ⬅️ ➡️ |
| Move Word | ctrl + ⬅️ ➡️ |
| Home | home, ctrl+a |
| End | end, ctrl+e |
| Page Up | pageup |
| Page Down | pagedown |
| |
| Select | Shift + ⬆️ ⬇️ ⬅️ ➡️ |
| Select Word | ctrl + shift + ⬅️ ➡️ |
| Select to Line Start | shift+home |
| Select to Line End | shift+end |
| Select Line | f6 |
| Select All | F7 |
| |
| Delete Left | backspace |
| Delete Right | DEL, ctrl+d |
| Delete Word Left | ctrl+w |
| Delete Word Right | ctrl+f |
| Delete Line | ctrl+x |
| Delete Line Start | ctrl+u |
| Delete Line End | ctrl+k |

> Note that you can quickly execute menu items by typing escape then keybindings. (Eg, "escape, w, t" to change theme)

## Exit any dialog (including this one): Esc
"""

class Shortcuts(ModalScreen):
    CSS = """
    Shortcuts {
        align: center middle;
    }

    #dialog {
        height: 90%;
        width: 90%;
        border: solid;
        padding: 0;
        margin: 0;
    }
    
    MarkdownViewer {
        padding: 0;
        margin: 0;
    }
    """

    def compose(self) -> ComposeResult:
        shortcuts = SHORTCUTS.format(**config.settings['shortcuts'])
        with ScrollView(id="dialog"):
            with Horizontal():
                yield MarkdownViewer(shortcuts, show_table_of_contents=False)
