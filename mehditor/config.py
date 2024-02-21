import configparser
import os
import pathlib

DEFAULT_SETTINGS = {
    "shortcuts": {
        "menu": "escape",
        "quit": "ctrl+c",
        "new_file": "ctrl+n",
        "open_file": "ctrl+o",
        "save_file": "ctrl+s",
        "goto_line": "ctrl+g",
        "show_shortcuts": "f1",
        "cut": "f2",
        "copy": "f3",
        "paste": "f4",
        "undo_change": "ctrl+z",
        "redo_change": "ctrl+y",
        "suspend_process": "f9"
    },
    "filetypes": {
        "css": "css",
        "html": "html",
        "htm": "html",
        "xml": "html",
        "py": "python",
        "yaml": "yaml",
        "yml": "yaml",
        "json": "json",
        "markdown": "markdown",
        "md": "markdown",
        "sql": "sql",
        "toml": "toml",
        "regex": "regex",
    },
    "editing": {
        "indent_type": "spaces",
        "indent_width": 4,
        "theme": "dracula",
        "dark_mode": True,
        "show_line_numbers": True,
        "soft_wrap": False
    }
}

PRIORITY_SHORTCUTS = ["menu", "quit"]
SHOW_SHORTCUTS = ["menu", "show_shortcuts", "cut", "copy", "paste"]
SHORTCUT_ALTS = {
    "escape": "Esc",
}
SHORTCUT_ITEM_NAME_OVERRIDES = {
    "undo_change": "Undo",
    "redo_change": "Redo"
}
settings = configparser.ConfigParser()
settings.read_dict(DEFAULT_SETTINGS)


def generate_binding(item, show=None):
    from textual.binding import Binding
    name = SHORTCUT_ITEM_NAME_OVERRIDES.get(item, item.replace('_', ' ').title())

    if show is None:
        show = item in SHOW_SHORTCUTS

    return Binding(settings["shortcuts"][item], item, name, show=show, priority=item in PRIORITY_SHORTCUTS,
                   key_display=shortcut_alts(item))


def shortcut_alts(item):
    shortcut = settings["shortcuts"][item]
    return SHORTCUT_ALTS.get(shortcut, shortcut)


def load():
    config_paths = []

    f = get_default_config_file()
    if f:
        config_paths.append(f)

    if os.getenv('MEHEDITOR_CONFIG'):
        if pathlib.Path(os.getenv('MEHEDITOR_CONFIG')).exists():
            config_paths.append(pathlib.Path(os.getenv('MEHEDITOR_CONFIG')))
        else:
            raise FileNotFoundError(
                f"MEHEDITOR_CONFIG environment variable set to {os.getenv('MEHEDITOR_CONFIG')} but file does not exist")

    for path in config_paths:
        settings.read(path)


def get_default_config_file():
    if os.name == 'nt':
        return pathlib.Path(os.getenv('APPDATA')) / 'mehditor' / 'mehditor.cfg'
    elif os.name == 'posix':
        return pathlib.Path(os.getenv('XDG_CONFIG_HOME',
                                      pathlib.Path(os.path.expanduser("~")) / '.config')) / 'mehditor' / 'mehditor.cfg'


def save():
    f = get_default_config_file()
    if not f:
        raise FileNotFoundError("Could not find default config file")
    f.parent.mkdir(parents=True, exist_ok=True)
    with open(f, 'w') as fp:
        settings.write(fp)
    return f


load()

__ALL__ = ['settings', 'shortcut_alts', 'load', 'save']
