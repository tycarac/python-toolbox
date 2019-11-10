import logging


# _____________________________________________________________________________
class NoExceptionFormatter(logging.Formatter):
    """
    Remove exception details from logger formatter so to declutter log output
    """
    def format(self, record):
        record.exc_text = ''
        # ensure formatException gets called
        return super(NoExceptionFormatter, self).format(record)

    def formatException(self, record):
        return ''
