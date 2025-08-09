frappe.ui.form.on('Customer Profile', {
	refresh: function(frm) {
		// Add custom buttons
		if (frm.doc.payment_status === 'Pending') {
			frm.add_custom_button(__('Mark as Paid'), function() {
				frm.set_value('payment_status', 'Paid');
				frm.set_value('payment_date', frappe.datetime.get_today());
				frm.save();
			}, __('Payment'));
		}
		
		if (frm.doc.service_status === 'Pending') {
			frm.add_custom_button(__('Activate Service'), function() {
				frm.set_value('service_status', 'Active');
				frm.save();
			}, __('Service'));
		}
	},
	
	payment_status: function(frm) {
		// Auto-update service status based on payment
		if (frm.doc.payment_status === 'Paid') {
			frm.set_value('service_status', 'Active');
		} else if (frm.doc.payment_status === 'Pending') {
			frm.set_value('service_status', 'Pending');
		}
	},
	
	cnic: function(frm) {
		if (frm.doc.cnic && frm.doc.cnic.length !== 13) {
			frappe.msgprint(__('CNIC must be exactly 13 digits'));
		}
	}
});

frappe.ui.form.on('Customer Package', {
	package: function(frm, cdt, cdn) {
		// Auto-fetch package details when package is selected
		var row = locals[cdt][cdn];
		if (row.package) {
			frappe.call({
				method: 'frappe.client.get',
				args: {
					doctype: 'Package',
					name: row.package
				},
				callback: function(r) {
					if (r.message) {
						frappe.model.set_value(cdt, cdn, 'package_name', r.message.package_name);
						frappe.model.set_value(cdt, cdn, 'price', r.message.price);
						frm.refresh_field('selected_packages');
						calculate_total(frm);
					}
				}
			});
		}
	},
	
	selected_packages_remove: function(frm) {
		calculate_total(frm);
	}
});

function calculate_total(frm) {
	var total = 0;
	frm.doc.selected_packages.forEach(function(row) {
		total += row.price || 0;
	});
	frm.set_value('total_amount', total);
}