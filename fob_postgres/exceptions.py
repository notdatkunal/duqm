#
# class PostgresError(Exception):
#     def __init__(self,message):
#         # super.__init__(message)
#         ...


class PostgresError(Exception):
    def __init__(self, code: int, message: str = 'POSTGRES_ERROR', details: dict | None = None):
        self.code = code
        self.message = message
        self.details = details

    def to_dict(self):
        """
        convert error into JSON serializable dict
        """
        return {
            'code': self.code
            , 'message': self.message
            , 'details': self.details if self.details is not None else ''
        }