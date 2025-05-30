
class UserInputError(Exception):
    def __init__(self, message, status_code=400):
        self.status_code = status_code
        super().__init__(message)
