#!/usr/bin/env python3

class ConnectionError(BaseException):
    pass


class AuthError(BaseException):
    pass

class RequestError(BaseException):
    pass

class DataError(BaseException):
    pass
