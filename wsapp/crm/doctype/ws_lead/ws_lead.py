import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime


class WSLead(Document):
    def validate(self):
        self.set_full_name()
        self.validate_email()

    def set_full_name(self):
        self.full_name = " ".join(
            filter(None, [self.first_name, self.last_name])
        )

    def validate_email(self):
        if self.email_id:
            from frappe.utils import validate_email_address
            if not validate_email_address(self.email_id):
                frappe.throw(frappe._("Invalid Email Address: {0}").format(self.email_id))

    @frappe.whitelist()
    def convert_to_customer(self):
        """Convert Lead to Customer"""
        if self.status == "Converted":
            frappe.throw(frappe._("Lead is already converted to Customer"))

        customer = frappe.new_doc("WS Kontakt")
        customer.kontakt_name = self.company_name or self.full_name
        customer.email_id = self.email_id
        customer.mobile_no = self.mobile_no
        customer.phone = self.phone
        customer.website = self.website
        customer.territory = self.territory
        customer.lead_name = self.name
        customer.insert(ignore_permissions=True)

        self.status = "Converted"
        self.customer = customer.name
        self.save(ignore_permissions=True)

        return customer.name
