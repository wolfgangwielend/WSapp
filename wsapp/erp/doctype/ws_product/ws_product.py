import frappe
from frappe.model.document import Document


class WSProduct(Document):
    def validate(self):
        if self.standard_rate and self.standard_rate < 0:
            frappe.throw(frappe._("Standard Rate cannot be negative"))
        if self.valuation_rate and self.valuation_rate < 0:
            frappe.throw(frappe._("Valuation Rate cannot be negative"))
