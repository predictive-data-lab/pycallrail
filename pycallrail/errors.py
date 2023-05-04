class LightValidationError(Exception):
    def __init__(self, message: str) -> None:
        super(LightValidationError, self).__init__(message)
