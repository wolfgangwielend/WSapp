import frappe


def before_install():
    pass


def after_install():
    create_default_roles()
    create_default_data()


def create_default_roles():
    roles = ["CRM User", "CRM Manager", "ERP User", "ERP Manager"]
    for role in roles:
        if not frappe.db.exists("Role", role):
            frappe.get_doc({"doctype": "Role", "role_name": role}).insert(ignore_permissions=True)
    frappe.db.commit()


def create_default_data():
    frappe.db.commit()
