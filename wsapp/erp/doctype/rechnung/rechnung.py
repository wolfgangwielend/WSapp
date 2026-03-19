import frappe
from frappe.model.document import Document


class Rechnung(Document):
    def before_save(self):
        self.berechne_summen()

    def berechne_summen(self):
        nettosumme = 0
        rabatt_gesamt = 0
        mwst_betrag = 0

        for pos in self.items:
            brutto_pos = (pos.menge or 0) * (pos.einzelpreis or 0)
            rabatt_betrag = brutto_pos * ((pos.rabatt or 0) / 100)
            netto_pos = brutto_pos - rabatt_betrag
            mwst_pos = netto_pos * (float(pos.mwst_satz or 0) / 100)

            pos.nettobetrag = netto_pos
            pos.gesamtbetrag = netto_pos + mwst_pos

            nettosumme += netto_pos
            rabatt_gesamt += rabatt_betrag
            mwst_betrag += mwst_pos

        self.nettosumme = nettosumme
        self.rabatt_gesamt = rabatt_gesamt
        self.mwst_betrag = mwst_betrag
        self.gesamtsumme = nettosumme + mwst_betrag

    def on_submit(self):
        self.status = "Versendet"

    def on_cancel(self):
        self.status = "Storniert"
