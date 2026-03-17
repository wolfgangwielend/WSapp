import frappe
from frappe.model.document import Document


class WSCustomer(Document):
    def validate(self):
        self.validate_email()

    def validate_email(self):
        if self.email_id:
            from frappe.utils import validate_email_address
            if not validate_email_address(self.email_id):
                frappe.throw(frappe._("Invalid Email Address: {0}").format(self.email_id))

    def after_insert(self):
        # Link lead to customer if created from lead
        if self.lead_name:
            frappe.db.set_value("WS Lead", self.lead_name, "status", "Converted")
            frappe.db.set_value("WS Lead", self.lead_name, "customer", self.name)
