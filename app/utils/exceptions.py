class NotFoundError(ValueError):
    def __init__(self, message):
        super().__init__(message)

class DuplicateValueError(ValueError):
    def __init__(self, message):
        super().__init__(message)

class InvalidDataError(ValueError):
    def __init__(self, message):
        super().__init__(message)