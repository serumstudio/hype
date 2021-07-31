

class HypeException(Exception):
    def __init__(self, msg=None):
        if msg == None:
            msg = "Something went wrong with the Hype CLI"

        super().__init__(msg)


class OptionError(HypeException):
    def __init__(self, msg="There is something went wrong on the option"):
        super().__init__(msg)

class TooMuchArguments(HypeException):
    def __init__(self, msg="You passed too much arguments"):
        super().__init__(msg)


class PluginError(HypeException):
    def __init__(self, msg="Plugin not installed"):
        super().__init__(msg)