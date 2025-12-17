class ChallengeNotFound(Exception):
    """
    Raised when a challenge cannot be found.
    """
    pass

class ChallengeInvalidStatus(Exception):
    """
    Raised when a challenge status cannot be validated.
    """
    pass

class ChallengeStatusAlreadyException(Exception):
    pass

