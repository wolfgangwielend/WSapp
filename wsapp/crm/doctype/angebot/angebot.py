import frappe
from frappe.model.document import Document


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
