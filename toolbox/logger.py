import logging


# _____________________________________________________________________________
class NoExceptionFormatter(logging.Formatter):
    """Remove exception details from logger formatter so to declutter log output
    """
    def format(self, record):
        record.exc_text = ''
        return super(NoExceptionFormatter, self).format(record)

    def formatException(self, exc_info):
        return ''


# _____________________________________________________________________________
class OneLineExceptionFormatter(logging.Formatter):
    """Covert exception details to single line to simplify log output processing
    """
    def format(self, record):
        text = super().format(record)
        if record.exc_text:
            text = text.replace('\n', '|')
        return text

    def formatException(self, exc_info):
        return repr(super().formatException(exc_info))
