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
COMPANY_OWNER = ['edit', 'publish', 'un_publish', 'upload_files', 'delete_files', 'add_employee',
                 'suspend_employee', 'send_publications', 'manage_access_company', 'manage_access_portal',
                 'article_priority', 'manage_readers', 'manage_companies_partners', 'manage_comments']

class RIGHTS:

    def EDIT(self):
        return 'edit'

    def PUBLISH(self):
        return 'publish'

    def UNPUBLISH(self):
        return 'un_publish'

    def UPLOAD_FILES(self):
        return 'upload_files'

    def DELETE_FILES(self):
        return 'delete_files'

    def ADD_EMPLOYEE(self):
        return 'add_employee'

    def SUSPEND_EMPLOYEE(self):
        return 'suspend_employee'

    def SEND_PUBLICATIONS(self):
        return 'send_publications'

    def MANAGE_ACCESS_COMPANY(self):
        return 'manage_access_company'

    def MANAGE_ACCESS_PORTAL(self):
        return 'manage_access_portal'

    def ARTICLE_PRIORITY(self):
        return 'article_priority'

    def MANAGE_READERS(self):
        return 'manage_readers'

    def MANAGE_COMPANIES_PARTNERS(self):
        return 'manage_companies_partners'

    def MANAGE_COMMENTS(self):
        return 'manage_comments'

    def SUBSCRIBE_TO_PORTALS(self):
        return 'subscribe_to_portals'
