import frappe
from frappe.model.document import Document


class Lieferschein(Document):
    def on_submit(self):
        self.status = "Geliefert"

    def on_cancel(self):
        self.status = "Storniert"
