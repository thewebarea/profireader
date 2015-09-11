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

COMPANY_OWNER_RIGHTS = 0x7fffffffffffffff  # 2**63-1

class RIGHTS:

    @staticmethod
    def EDIT():
        return 'edit'

    @staticmethod
    def PUBLISH():
        return 'publish'

    @staticmethod
    def UNPUBLISH():
        return 'un_publish'

    @staticmethod
    def UPLOAD_FILES():
        return 'upload_files'

    @staticmethod
    def DELETE_FILES():
        return 'delete_files'

    @staticmethod
    def ADD_EMPLOYEE():
        return 'add_employee'

    @staticmethod
    def SUSPEND_EMPLOYEE():
        return 'suspend_employee'

    @staticmethod
    def SEND_PUBLICATIONS():
        return 'send_publications'

    @staticmethod
    def MANAGE_ACCESS_COMPANY():
        return 'manage_access_company'

    @staticmethod
    def MANAGE_ACCESS_PORTAL():
        return 'manage_access_portal'

    @staticmethod
    def ARTICLE_PRIORITY():
        return 'article_priority'

    @staticmethod
    def MANAGE_READERS():
        return 'manage_readers'

    @staticmethod
    def MANAGE_COMPANIES_PARTNERS():
        return 'manage_companies_partners'

    @staticmethod
    def MANAGE_COMMENTS():
        return 'manage_comments'

    @staticmethod
    def SUBSCRIBE_TO_PORTALS():
        return 'subscribe_to_portals'
