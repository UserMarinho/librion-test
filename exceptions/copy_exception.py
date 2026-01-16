class IsbnNotFoundError(Exception):
    pass

class CopyNotFoundError(Exception):
    pass

class CopyAlreadyExistsError(Exception):
    pass

class CopyOutOfStock(Exception):
    pass