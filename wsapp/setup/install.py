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
    # Create default customer groups
    groups = ["Commercial", "Individual", "Government"]
    for group in groups:
        if not frappe.db.exists("Customer Group", group):
            frappe.get_doc({
                "doctype": "Customer Group",
                "customer_group_name": group,
                "parent_customer_group": "All Customer Groups"
            }).insert(ignore_permissions=True)

    frappe.db.commit()
