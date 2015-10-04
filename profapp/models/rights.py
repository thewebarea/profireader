from functools import reduce
import inspect
from ..controllers import errors
import collections

#COMPANY_OWNER = ['edit', 'publish', 'unpublish', 'upload_files', 'delete_files', 'add_employee',
#                 'suspend_employee', 'submit_publications', 'manage_rights_company', 'manage_portal',
#                 'article_priority', 'manage_readers', 'manage_companies_members', 'manage_comments',
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
    def UPLOAD_FILES():
        return 'upload_files'

    @staticmethod
    def SUBMIT_PUBLICATIONS():
        return 'submit_publications'

    @staticmethod
    def ACCEPT_REFUSE_PUBLICATION():
        return 'accept_refuse_publication'

    @staticmethod
    def PUBLISH():
        return 'publish'

    @staticmethod
    def UNPUBLISH():
        return 'un_publish'

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
    def SUBSCRIBE_TO_PORTALS():
        return 'subscribe_to_portals'

    @staticmethod
    def MANAGE_RIGHTS_COMPANY():
        return 'manage_rights_company'

    @staticmethod
    def EDIT():
        return 'edit'

    @staticmethod
    def MANAGE_PORTAL():
        return 'manage_portal'

    @staticmethod
    def ARTICLE_PRIORITY():
        return 'article_priority'

    @staticmethod
    def MANAGE_READERS():
        return 'manage_readers'

    @staticmethod
    def REMOVE_PUBLICATION():
        return 'remove_publication'

    @staticmethod
    def MANAGE_COMMENTS():
        return 'manage_comments'

    @staticmethod
    def MANAGE_COMPANIES_MEMBERS():
        return 'manage_companies_members'


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
    UPLOAD_FILES = ('upload_files', 0x00008, "Upload files to company's folder", 1)
    SUBMIT_PUBLICATIONS = ('submit_publications', 0x00080, 'Submit materials to company', 2)
    ACCEPT_REFUSE_PUBLICATION = ('accept_refuse_publication', 0x08000, 'Accept or refuse submitted materials', 3)
    PUBLISH = ('publish', 0x00002, "Publish company's materials to portal", 4)
    UNPUBLISH = ('unpublish', 0x00004, "Unpublish company's publication from portal", 5)
    DELETE_FILES = ('delete_files', 0x00010, "Remove files from company's folder", 6)
    ADD_EMPLOYEE = ('add_employee', 0x00020, 'Approve new employee', 7)
    SUSPEND_EMPLOYEE = ('suspend_employee', 0x00040, 'Suspend and unsuspend employee', 8)
    SUBSCRIBE_TO_PORTALS = ('subscribe_to_portals', 0x04000, 'Apply company request for portal membership', 9)
    MANAGE_RIGHTS_COMPANY = ('manage_rights_company', 0x00100, 'Change rights for company employees', 10)
    EDIT = ('edit', 0x00001, 'Edit company profile', 11)
    MANAGE_PORTAL = ('manage_portal', 0x00200, 'Create portal and manage portal divisions', 12)
    ARTICLE_PRIORITY = ('article_priority', 0x00400, 'Set publication priority on portal', 13)
    MANAGE_READERS = ('manage_readers', 0x0800, 'Manage readers subscriptions', 14)
    REMOVE_PUBLICATION = ('remove_publication', 0x10000, 'Remove any publication from owned portal', 15)
    MANAGE_COMMENTS = ('manage_comments', 0x2000, 'Manages comments', 16)
    MANAGE_COMPANIES_MEMBERS = ('manage_companies_members', 0x01000, 'Accept or refuse company membership on portal', 17)

    # read this:
    # http://stackoverflow.com/questions/9058305/getting-attributes-of-a-class
    @classmethod
    def keys(cls, with_values=False):
        attributes = inspect.getmembers(cls, lambda a: not(inspect.isroutine(a)))
        if not with_values:
            return [a[0] for a in attributes if
                    not(a[0].startswith('__') and a[0].endswith('__'))]
        else:
            return [a for a in attributes if
                    not(a[0].startswith('__') and a[0].endswith('__'))]

    @classmethod
    def __getitem__(cls, attr):
        return getattr(cls, attr.upper())[0]

# list_of_RightAtomic_attributes = get_my_attributes(RightAtomic)


class RightHumnReadible(RightAtomic):
    @classmethod
    def __getitem__(cls, attr):
        return getattr(cls, attr.upper())[2]


class Right(RightAtomic):
    # renamed from RIGHTS

    @classmethod
    def VALUE_RIGHT(cls):
        return {getattr(RightAtomic, field)[1]: getattr(RightAtomic, field)[0]
                for field in RightAtomic.keys()}

    @classmethod
    def RIGHT_VALUE(cls):
        return {getattr(RightAtomic, field)[0]: getattr(RightAtomic, field)[1]
                for field in RightAtomic.keys()}

    @classmethod
    def RIGHT_POSITION(cls):
        return {getattr(RightAtomic, field)[0]: getattr(RightAtomic, field)[3]
                for field in RightAtomic.keys()}

    @classmethod
    def transform_rights_into_set(cls, rights_in_integer):
        rights_in_integer = rights_in_integer & ALL_AVAILABLE_RIGHTS_TRUE
        return \
            frozenset(
                [cls.VALUE_RIGHT()[2**position] for position, right in
                 enumerate(
                     list(map(int, list(bin(rights_in_integer)[2:][::-1])))
                 )
                 if right]
            )

    # TODO (AA to AA): check the correctness!!!
    @classmethod
    def transform_rights_into_integer(cls, rights_iterable):
        rez = reduce(lambda x, y: x | cls.RIGHT_VALUE()[y], rights_iterable, 0)
        return rez

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
