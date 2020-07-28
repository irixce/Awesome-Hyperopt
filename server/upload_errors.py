class UploadError(Exception):
    """Base class for other exceptions"""
    pass


# Flag exceptions

class InvalidFlag(UploadError):
    """Flag is invalid"""
    pass


class FileIsEmpty(UploadError):
    """File is empty!"""
    pass


# Model Configs exceptions

class InvalidModelTypes(UploadError):
    """Invalid model type(s)"""
    pass


class InvalidProblemTypes(UploadError):
    """Invalid problem type(s)"""
    pass


class InvalidAlgTypes(UploadError):
    """Invalid algorithm type(s)"""
    pass


class InvalidParamsTypes(UploadError):
    """Invalid parameter type(s)"""
    pass
