class CustomErorr(Exception):
    pass

class MissingManifestError(CustomErorr):
    pass

class InvalidRowError(CustomErorr):
    pass

class EmptyInputError(CustomErorr):
    pass