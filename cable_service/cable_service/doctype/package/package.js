frappe.ui.form.on('Package', {
	refresh: function(frm) {
		// Add custom buttons or functionality if needed
		if (frm.doc.is_active) {
			frm.add_custom_button(__('Deactivate'), function() {
				frm.set_value('is_active', 0);
				frm.save();
			});
		} else {
			frm.add_custom_button(__('Activate'), function() {
				frm.set_value('is_active', 1);
				frm.save();
			});
		}
	},
	
	price: function(frm) {
		if (frm.doc.price < 0) {
			frappe.msgprint(__('Price cannot be negative'));
			frm.set_value('price', 0);
		}
	}
});