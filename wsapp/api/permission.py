import frappe


def has_app_permission():
    """Check if current user has permission to access WS App"""
    return frappe.db.exists(
        "Has Role",
        {
            "parent": frappe.session.user,
            "role": ["in", ["CRM User", "CRM Manager", "ERP User", "ERP Manager", "System Manager", "Administrator"]],
        },
    )
