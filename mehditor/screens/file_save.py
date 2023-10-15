from mehditor.screens.file_chooser import FileChooser


class FileSave(FileChooser):
    CSS = """
        FileSave { 
            align: center middle;
        }
    """ + FileChooser.CSS

    def __init__(self, current_file, confirm_overwrite=True):
        super().__init__(current_file, confirm_overwrite)

