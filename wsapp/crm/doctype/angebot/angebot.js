frappe.ui.form.on('Angebot', {
	refresh(frm) {
		if (!frm.is_new() && frm.doc.status !== 'Abgelehnt' && frm.doc.status !== 'Abgelaufen') {
			frm.add_custom_button(__('Auftrag aus Angebot erzeugen'), function () {
				frappe.confirm(
					__('Soll aus dem Angebot <b>{0}</b> ein neuer Auftrag erstellt werden?', [frm.doc.name]),
					function () {
						frappe.call({
							method: 'wsapp.crm.doctype.angebot.angebot.make_auftrag',
							args: { angebot_name: frm.doc.name },
							freeze: true,
							freeze_message: __('Auftrag wird erstellt...'),
							callback: function (r) {
								if (r.message) {
									frappe.show_alert({
										message: __('Auftrag {0} wurde erstellt.', [r.message]),
										indicator: 'green'
									});
									frappe.set_route('Form', 'Auftrag', r.message);
								}
							}
						});
					}
				);
			}, __('Erstellen'));
		}
	}
});
