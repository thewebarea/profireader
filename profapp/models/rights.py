from functools import reduce
import inspect

#COMPANY_OWNER = ['edit', 'publish', 'unpublish', 'upload_files', 'delete_files', 'add_employee',
#                 'suspend_employee', 'send_publications', 'manage_access_company', 'manage_access_portal',
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
    EDIT = ('edit', 0x0001)
    PUBLISH = ('publish', 0x0002)
    UNPUBLISH = ('unpublish', 0x0004)
    UPLOAD_FILES = ('upload_files', 0x0008)
    DELETE_FILES = ('delete_files', 0x0010)
    ADD_EMPLOYEE = ('add_employee', 0x0020)
    SUSPEND_EMPLOYEE = ('suspend_employee', 0x0040)
    SEND_PUBLICATIONS = ('send_publications', 0x0080)
    MANAGE_ACCESS_COMPANY = ('manage_access_company', 0x0100)
    MANAGE_ACCESS_PORTAL = ('manage_access_portal', 0x0200)
    ARTICLE_PRIORITY = ('article_priority', 0x0400)
    MANAGE_READERS = ('manage_readers', 0x0800)
    MANAGE_COMPANIES_PARTNERS = ('manage_companies_partners', 0x1000)
    MANAGE_COMMENTS = ('manage_comments', 0x2000)
    SUBSCRIBE_TO_PORTALS = ('subscribe_to_portals', 0x4000)

    @classmethod
    def __getitem__(cls, attr):
        return getattr(cls, attr.upper())[0]

list_of_RightAtomic_attributes = get_my_attributes(RightAtomic)


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
        set_of_rights = set(rights_iterable)
        return reduce(lambda x, y: x |
                      cls.RIGHT_REVERSED[y], set_of_rights, 0)

#  we really need RightAtomic to be inherited from dict.
Right = Right()
# Now Right['edit'] returns 'edit'


# Base rights are added when user becomes confirmed in company
# BASE_RIGHTS_IN_COMPANY = 136
BASE_RIGHTS_IN_COMPANY = \
    Right.UPLOAD_FILES[1] | \
    Right.SEND_PUBLICATIONS[1]

# ALL_AVAILABLE_RIGHTS_TRUE = 32767
ALL_AVAILABLE_RIGHTS_TRUE = \
    reduce(lambda x, y: x | y,
           map(lambda x: x[1][1], get_my_attributes(RightAtomic, True)))

ALL_AVAILABLE_RIGHTS_FALSE = 0
