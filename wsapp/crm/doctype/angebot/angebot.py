import frappe
from frappe.model.document import Document


@frappe.whitelist()
def make_sales_order(angebot_name):
    angebot = frappe.get_doc("Angebot", angebot_name)

    so = frappe.new_doc("Sales Order")
    so.customer = angebot.kunde
    so.transaction_date = frappe.utils.today()
    so.terms = angebot.zahlungsbedingungen
    so.angebot = angebot.name

    for pos in angebot.positionen:
        so.append("items", {
            "item_name": pos.bezeichnung,
            "qty": pos.menge or 1,
            "uom": pos.einheit,
            "rate": pos.einzelpreis or 0,
            "discount_percentage": pos.rabatt or 0,
            "tax_rate": float(pos.mwst_satz or 0),
            "amount": pos.summe or 0,
            "grand_total": pos.gesamtsumme or 0,
        })

    so.total = angebot.nettosumme
    so.tax_amount = angebot.mwst_betrag
    so.grand_total = angebot.gesamtsumme
    so.insert()

    frappe.db.set_value("Angebot", angebot_name, "status", "Angenommen")

    return so.name


class Angebot(Document):
    def before_save(self):
        self.berechne_summen()

    def berechne_summen(self):
        nettosumme = 0
        rabatt_gesamt = 0
        mwst_betrag = 0

        for pos in self.positionen:
            brutto_pos = (pos.menge or 0) * (pos.einzelpreis or 0)
            rabatt_betrag = brutto_pos * ((pos.rabatt or 0) / 100)
            netto_pos = brutto_pos - rabatt_betrag
            mwst_pos = netto_pos * (float(pos.mwst_satz or 0) / 100)
            gesamt_pos = netto_pos + mwst_pos

            pos.summe = netto_pos
            pos.gesamtsumme = gesamt_pos

            nettosumme += netto_pos
            rabatt_gesamt += rabatt_betrag
            mwst_betrag += mwst_pos

        self.nettosumme = nettosumme
        self.rabatt_gesamt = rabatt_gesamt
        self.mwst_betrag = mwst_betrag
        self.gesamtsumme = nettosumme + mwst_betrag
