

class HTTPCodedException(Exception):
    status_code = 500


class FileTypeNotSupportedException(HTTPCodedException):
    status_code = 415

