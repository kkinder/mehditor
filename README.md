# Modern but simple text editor

Mehditor is a modern but simple text editor. I made it because I needed a quick editor (like Pico or Nano) on servers,
but wanted a more modern and friendly interface. Meditor is written in Python and uses the excellent
 [Textual](https://textual.textualize.io) for its user interface. I wrote it in a weekend.

![Mehditor screenshot showing application in terminal window](https://github.com/kkinder/mehditor/blob/main/screenshots/meh-1.png)

![Mehditor screenshot showing application in terminal window](https://github.com/kkinder/mehditor/blob/main/screenshots/meh-2.png)

![Mehditor screenshot showing application in terminal window](https://github.com/kkinder/mehditor/blob/main/screenshots/meh-3.png)

## Features

- Put that VGA graphics card to use with astonishing _color_ (light and dark modes!)
- Mouse support
- Modern-ish user interface with command palette and menus
- Undo/redo support (now updated with Textual's new undo/redo)
- Sensible keyboard shortcuts that work well over ssh, tmux, etc
- Syntax highlighting for Python, SQL, and more
- Easy installation via pip -- no root needed

## Drawbacks (what's missing)

- Made in a weekend, probably not ideal for heavy lifting
- Fairly minimal without features like multiple files or support for a lot of languages
- Written in Python, so probably not the most lightweight choice

## Installation

```
pip install -U mehditor
```

## Usage

```
meh <filename>
```

