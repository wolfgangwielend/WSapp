import frappe
from frappe.model.document import Document


class Auftrag(Document):
    def validate(self):
        self.calculate_totals()

    def calculate_totals(self):
        total_qty = 0
        total = 0
        tax_amount = 0

        for item in self.items:
            item.amount = (item.qty or 0) * (item.rate or 0)
            total_qty += item.qty or 0
            total += item.amount or 0
            if item.tax_rate:
                tax_amount += item.amount * (item.tax_rate / 100)

        self.total_quantity = total_qty
        self.total = total
        self.tax_amount = tax_amount
        self.grand_total = total + tax_amount

    def on_submit(self):
        self.status = "Confirmed"

    def on_cancel(self):
        self.status = "Cancelled"
