from textual.validation import Integer


def is_line_number(value: str):
    """Check if the input is a line number."""
    if value.count(":") == 1:
        line, col = value.split(':', 1)
        return Integer(minimum=1).validate(line) and Integer(minimum=1).validate(col)
    elif value.count(":") == 0:
        return Integer(minimum=1).validate(value)
    else:
        return False
