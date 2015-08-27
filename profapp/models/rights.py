#COMPANY_OWNER = ['edit', 'publish', 'un_publish', 'upload_files', 'delete_files', 'add_employee',
#                 'suspend_employee', 'send_publications', 'manage_access_company', 'manage_access_portal',
#                 'article_priority', 'manage_readers', 'manage_companies_partners', 'manage_comments']


class Right:  # renamed from RIGHTS
    EDIT = 0x0001
    PUBLISH = 0x0002
    UNPUBLISH = 0x0004
    UPLOAD_FILES = 0x0008
    DELETE_FILES = 0x0010
    ADD_EMPLOYEE = 0x0020
    SUSPEND_EMPLOYEE = 0x0040
    SEND_PUBLICATIONS = 0x0080
    MANAGE_ACCESS_COMPANY = 0x0100
    MANAGE_ACCESS_PORTAL = 0x0200
    ARTICLE_PRIORITY = 0x0400
    MANAGE_READERS = 0x0800
    MANAGE_COMPANIES_PARTNERS = 0x1000
    MANAGE_COMMENTS = 0x2000
    SUBSCRIBE_TO_PORTALS = 0x4000

    COMPANY_OWNER = 0x8000000000000000  # 2**63

#Base rights are added when user becomes confirmed in company
BASE_RIGHTS_IN_COMPANY = \
    Right.UPLOAD_FILES | \
    Right.SEND_PUBLICATIONS
