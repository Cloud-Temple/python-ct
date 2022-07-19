# coding: utf-8


class ServiceException(Exception):
    def __init__(self, message, reason=None):
        self.message = message
        self.reason = reason

    def __str__(self):
        if self.reason is not None:
            return "%s - %s" % (self.message, str(self.reason))
        return self.message
