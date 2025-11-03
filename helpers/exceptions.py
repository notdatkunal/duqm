class AppException(Exception):
    def __init__(self, message, error_code):
        self.message = {message}
        self.error_code = error_code
        super().__init__(self.message)


class TokenExpiredException(Exception):
    def __init__(self, message='token has been expired'):
        self.message = message
        super().__init__(self.message)


class NotFoundAppException(Exception):
    def __init__(self, message='no data found'):
        self.message = message
        super().__init__(self.message)


class BadRequestException(Exception):
    def __init__(self, message='no data found'):
        self.message = message
        super().__init__(self.message)


class UnAuthorizedException(Exception):
    def __init__(self, message='Unauthorized'):
        self.message = message
        super().__init__(self.message)
