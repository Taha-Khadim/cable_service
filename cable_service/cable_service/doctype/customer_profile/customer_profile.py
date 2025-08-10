import frappe
from frappe.model.document import Document
import json

class CustomerProfile(Document):
	def validate(self):
		if self.cnic and len(str(self.cnic)) != 13:
			frappe.throw("CNIC must be 13 digits")
		
		# Validate phone number
		if not self.phone:
			frappe.throw("Phone number is required")
		
		# Auto-set status based on payment
		if self.payment_status == "Paid":
			self.service_status = "Active"
		elif self.payment_status == "Pending":
			self.service_status = "Pending"
		elif self.payment_status == "Partial":
			self.service_status = "Inactive"
		else:
			self.service_status = "Pending"
	
	def before_save(self):
		# Calculate total amount based on selected packages
		total = 0
		if self.selected_packages:
			for package in self.selected_packages:
				if package.price:
					total += package.price
				elif package.package:
					try:
						package_doc = frappe.get_doc("Package", package.package)
						total += package_doc.price
						package.price = package_doc.price
						package.package_name = package_doc.package_name
					except:
						pass
		self.total_amount = total
		
		# Set created_by if not set
		if not self.created_by:
			self.created_by = frappe.session.user