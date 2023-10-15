# from textual.containers import Vertical, Horizontal
# from textual.screen import ModalScreen
# from textual.widgets import Button, Label, Checkbox, ListView, ListItem
# from textual.widgets import Input
#
#
# class FileSettings(ModalScreen):
#     CSS = """
#     FileSettings {
#         align: center middle;
#     }
#
#     #dialog {
#         padding: 0;
#         width: 50;
#         height: 10;
#         border: thick $background 80%;
#         background: $surface;
#     }
#     """
#
#     def __init__(self, settings, language_choices):
#         super().__init__()
#
#         self.settings = settings
#         self.language_choices = language_choices
#
#         if self.settings["file_type"] in self.language_choices:
#             self.language_index = self.language_choices.index(self.settings["file_type"])
#         else:
#             self.language_index = 0
#
#     def compose(self):
#         with Vertical(id="dialog"):
#             yield Label("File Settings", id="title")
#             yield Checkbox("Use spaces instead of tabs", self.settings["ident_type"] == "spaces", id="use-spaces")
#             with Horizontal():
#                 yield Label("Indent width: ", id="tab-width-label")
#                 yield Input(str(self.settings["tab_width"]), id="tab-width")
#             with Horizontal():
#                 yield Label("File Type: ", id="indent-width-label")
#                 yield ListView(*[ListItem(Label(label), id=i, classes="choices") for i, label in self.language_choices],
#                                id="choices", classes="choices", initial_index=self.language_index)
#
#     def on_button_pressed(self, event: Button.Pressed) -> None:
#         self.dismiss()
