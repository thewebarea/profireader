from functools import reduce
import inspect
from ..controllers import errors
import collections

#COMPANY_OWNER = ['edit', 'publish', 'unpublish', 'upload_files', 'delete_files', 'add_employee',
#                 'suspend_employee', 'submit_publications', 'manage_rights_company', 'manage_rights_portal',
#                 'article_priority', 'manage_readers', 'manage_companies_partners', 'manage_comments',
#                 'subscribe_to_portals']


# ROLE = {
#     OWNER: 'owner',
#     ADMIN: 'admin',
#     EDITOR: 'editor',
#     STAFF: 'staff',
#     CONTRIBUTOR: 'contributor',
#     USER: 'user',
#     GUEST: 'guest',
#     READER: 'reader'
# }


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
    def SUBMIT_PUBLICATIONS():
        return 'submit_publications'

    @staticmethod
    def MANAGE_RIGHTS_COMPANY():
        return 'manage_rights_company'

    @staticmethod
    def MANAGE_RIGHTS_PORTAL():
        return 'manage_rights_portal'

    @staticmethod
    def ARTICLE_PRIORITY():
        return 'article_priority'

    # @staticmethod
    # def MANAGE_READERS():
    #     return 'manage_readers'

    @staticmethod
    def MANAGE_COMPANIES_PARTNERS():
        return 'manage_companies_partners'

    # @staticmethod
    # def MANAGE_COMMENTS():
    #     return 'manage_comments'

    @staticmethod
    def SUBSCRIBE_TO_PORTALS():
        return 'subscribe_to_portals'

    @staticmethod
    def ACCEPT_REFUSE_PUBLICATION():
        return 'accept_refuse_publication'


# read this:
# http://stackoverflow.com/questions/9058305/getting-attributes-of-a-class
def get_my_attributes(my_class, with_values=False):
    attributes = inspect.getmembers(my_class,
                                    lambda a: not(inspect.isroutine(a)))
    if not with_values:
        return [a[0] for a in attributes if
                not(a[0].startswith('__') and a[0].endswith('__'))]
    else:
        return [a for a in attributes if
                not(a[0].startswith('__') and a[0].endswith('__'))]


class RightAtomic(dict):
    EDIT = ('edit', 0x0001, 'Can edit company profile and manage files in company corporate folder')
    PUBLISH = ('publish', 0x0002, 'Can publish submited materials to portal')
    UNPUBLISH = ('unpublish', 0x0004, 'Can unpublish publication from portal')
    UPLOAD_FILES = ('upload_files', 0x0008, 'Can upload files to journalist materials folder')
    DELETE_FILES = ('delete_files', 0x0010, 'Can remove files from journalist materials folder')
    ADD_EMPLOYEE = ('add_employee', 0x0020, 'Can approve new employee')
    SUSPEND_EMPLOYEE = ('suspend_employee', 0x0040, 'Can suspend employee')
    SUBMIT_PUBLICATIONS = ('submit_publications', 0x0080, 'Can submit publication to employer company')
    MANAGE_RIGHTS_COMPANY = ('manage_rights_company', 0x0100, 'Can change rights for employee (red rights)')
    MANAGE_RIGHTS_PORTAL = ('manage_rights_portal', 0x0200, 'Can change rights for partner company in portal (blue rights)')
    ARTICLE_PRIORITY = ('article_priority', 0x0400, 'Can set article priority')
    # MANAGE_READERS = ('manage_readers', 0x0800, 'Manage readers')
    MANAGE_COMPANIES_PARTNERS = ('manage_companies_partners', 0x1000, 'Accept or refuse partnership request')
    # MANAGE_COMMENTS = ('manage_comments', 0x2000)
    SUBSCRIBE_TO_PORTALS = ('subscribe_to_portals', 0x4000, 'Apply request for company partnership')
    ACCEPT_REFUSE_PUBLICATION = ('accept_refuse_publication', 0x8000, 'Accept or refuse submitted publication')


    @classmethod
    def __getitem__(cls, attr):
        return getattr(cls, attr.upper())[0]

list_of_RightAtomic_attributes = get_my_attributes(RightAtomic)

class RightHumnReadible(RightAtomic):
    @classmethod
    def __getitem__(cls, attr):
        return getattr(cls, attr.upper())[2]

class Right(RightAtomic):
    # renamed from RIGHTS
    RIGHT = \
        {getattr(RightAtomic, field)[1]: getattr(RightAtomic, field)[0]
            for field in list_of_RightAtomic_attributes}
    RIGHT_REVERSED = \
        {getattr(RightAtomic, field)[0]: getattr(RightAtomic, field)[1]
            for field in list_of_RightAtomic_attributes}

    @classmethod
    def transform_rights_into_set(cls, rights_in_integer):
        rights_in_integer = rights_in_integer & ALL_AVAILABLE_RIGHTS_TRUE
        return \
            frozenset(
                [cls.RIGHT[2**position] for position, right in
                 enumerate(
                     list(map(int, list(bin(rights_in_integer)[2:][::-1])))
                 )
                 if right]
            )

    # TODO (AA to AA): check the correctness!!!
    @classmethod
    def transform_rights_into_integer(cls, rights_iterable):
        rez = reduce(lambda x, y: x |
                     cls.RIGHT_REVERSED[y], rights_iterable, 0)
        return rez

    @staticmethod
    def check_type_rights_int(rights):
        return type(rights) == tuple and \
            len(rights) == 2 and \
            type(rights[0]) == int and \
            type(rights[1]) == int

    @staticmethod
    def check_type_rights_iterable(rights):
        return type(rights) == tuple and \
            len(rights) == 2 and \
            isinstance(rights[0], collections.Iterable) and \
            isinstance(rights[1], collections.Iterable)

#  we really need RightAtomic to be inherited from dict.
Right = Right()
RightHumnReadible = RightHumnReadible()
# Now Right['edit'] returns 'edit'


# Base rights are added when user becomes confirmed in company
# BASE_RIGHTS_IN_COMPANY = 136
BASE_RIGHTS_IN_COMPANY = \
    Right.UPLOAD_FILES[1] | \
    Right.SUBMIT_PUBLICATIONS[1]

# ALL_AVAILABLE_RIGHTS_TRUE = 32767
ALL_AVAILABLE_RIGHTS_TRUE = \
    reduce(lambda x, y: x | y,
           map(lambda x: x[1][1], get_my_attributes(RightAtomic, True)))

ALL_AVAILABLE_RIGHTS_FALSE = 0
