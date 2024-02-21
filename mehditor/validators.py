from textual.validation import Integer, Validator, Failure, ValidationResult


class LineNumber(Validator):
    class NotALineNumber(Failure):
        pass

    def validate(self, value: str):
        if value.count(":") == 1:
            line, col = value.split(':', 1)
            return Integer(minimum=1).validate(line) and Integer(minimum=1).validate(col)
        elif value.count(":") == 0:
            return Integer(minimum=1).validate(value)
        else:
            return ValidationResult.failure([LineNumber.NotALineNumber(self, value)])

    def describe_failure(self, failure: Failure):
        return "Must be a line number (with optional column); eg 10:3 for line 10, col 3"
