OWNER = 0
ADMIN = 1
EDITOR = 2
STAFF = 3
CONTRIBUTOR = 4
USER = 5
GUEST = 6
READER = 7

ROLE = {
    OWNER: 'owner',
    ADMIN: 'admin',
    EDITOR: 'editor',
    STAFF: 'staff',
    CONTRIBUTOR: 'contributor',
    USER: 'user',
    GUEST: 'guest',
    READER: 'reader'
}


COMPANY_OWNER_RIGHTS = 0x7fffffffffffffff # 2**63-1

GOD_RIGHTS = COMPANY_OWNER_RIGHTS  # the same as above but it is applied globally
