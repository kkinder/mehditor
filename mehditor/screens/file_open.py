from mehditor.screens.file_chooser import FileChooser


class FileOpen(FileChooser):
    CSS = """
    FileOpen { 
        align: center middle;
    }
    """ + FileChooser.CSS