import frappe
from frappe.model.document import Document

class CustomerProfile(Document):
	def validate(self):
		if len(self.cnic) != 13:
			frappe.throw("CNIC must be 13 digits")
		
		# Auto-set status based on payment
		if self.payment_status == "Paid":
			self.service_status = "Active"
		elif self.payment_status == "Pending":
			self.service_status = "Pending"
		else:
			self.service_status = "Inactive"
	
	def before_save(self):
		# Calculate total amount based on selected packages
		total = 0
		for package in self.selected_packages:
			package_doc = frappe.get_doc("Package", package.package)
			total += package_doc.price
		self.total_amount = total