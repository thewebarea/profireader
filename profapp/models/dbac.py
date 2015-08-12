class RBAC:
    def __init__(self):
        pass

def allow_company_operation(user_id, company_id, operation_id):
    pass

def deny_company_operation(user_id, company_id, operation_id):
    pass

def has_access(user_id, company_id, operation_id):
    return True

def allow_default_operations(user_id, company_id, role_id):
    if role_id == 'member':
        allow_company_operation(user_id, company_id, 'publish')
        allow_company_operation(user_id, company_id, 'unpublish')
    if role_id == 'redactor':
        allow_company_operation(user_id, company_id, 'manage_content')
    if role_id == 'hr':
        allow_company_operation(user_id, company_id, 'manage_members')
    if role_id == 'admin':
        allow_company_operation(user_id, company_id, 'manage_access')
    if role_id == 'owner':
        allow_company_operation(user_id, company_id, 'transfer_ownership')



    pass

