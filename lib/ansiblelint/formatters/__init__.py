class Formatter:

    def format(self, match):
        formatstr = "[{0}] {1}\n{2}:{3}\n{4}\n"
        return formatstr.format(match.rule.id,
                                match.message,
                                match.filename,
                                match.linenumber,
                                match.line)


class QuietFormatter:

    def format(self, match):
        formatstr = "[{0}] {1}:{2}"
        return formatstr.format(match.rule.id, match.filename,
                                match.linenumber)
