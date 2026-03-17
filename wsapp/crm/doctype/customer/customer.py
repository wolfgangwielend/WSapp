import frappe
from frappe.model.document import Document


class WSCustomer(Document):
    def before_save(self):
        self.set_customer_name()

    def set_customer_name(self):
        parts = []
        if self.titel_davor:
            parts.append(self.titel_davor)
        if self.vorname:
            parts.append(self.vorname)
        if self.nachname:
            parts.append(self.nachname)
        if self.titel_danach:
            parts.append(self.titel_danach)
        if parts:
            self.customer_name = " ".join(parts)
        elif not self.customer_name:
            self.customer_name = self.name

    def validate(self):
        self.validate_email()

    def validate_email(self):
        if self.email_id:
            from frappe.utils import validate_email_address
            if not validate_email_address(self.email_id):
                frappe.throw(frappe._("Ungültige E-Mail-Adresse: {0}").format(self.email_id))
        if self.email_2:
            from frappe.utils import validate_email_address
            if not validate_email_address(self.email_2):
                frappe.throw(frappe._("Ungültige E-Mail-Adresse 2: {0}").format(self.email_2))
