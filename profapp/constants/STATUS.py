class STATUS_NAME(dict):
    ACTIVE = ('active', 1)
    NONACTIVE = ('nonactive', 2)
    BLOCKED = ('blocked', 3)
    DELETED = ('deleted', 4)
    BANNED = ('banned', 5)
    REJECTED = ('rejected', 6)
    SUSPENDED = ('suspended', 7)

    @classmethod
    def __getitem__(cls, attr):
        return getattr(cls, attr.upper())[0]

STATUS_NAME = STATUS_NAME()


class STATUS:

    @staticmethod
    def NONACTIVE():
        return 'nonactive'

    @staticmethod
    def ACTIVE():
        return 'active'

    @staticmethod
    def BLOCKED():
        return 'blocked'

    @staticmethod
    def DELETED():
        return 'deleted'

    @staticmethod
    def BANNED():
        return 'banned'

    @staticmethod
    def REJECTED():
        return 'rejected'

    @staticmethod
    def SUSPENDED():
        return 'suspended'
