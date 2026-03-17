import frappe
from frappe.model.document import Document


class WSOpportunity(Document):
    def validate(self):
        self.validate_customer_or_lead()
        self.calculate_weighted_value()

    def validate_customer_or_lead(self):
        if not self.customer and not self.lead:
            frappe.throw(frappe._("Please set either a Customer or a Lead"))

    def calculate_weighted_value(self):
        if self.expected_value and self.probability:
            self.weighted_value = (self.expected_value * self.probability) / 100
