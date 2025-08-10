import frappe
from frappe.model.document import Document

class Package(Document):
	def validate(self):
		if self.price and self.price < 0:
			frappe.throw("Price cannot be negative")
		
		if not self.package_name:
			frappe.throw("Package name is required")
		
		# Check for duplicate package names
		existing = frappe.db.exists('Package', {'package_name': self.package_name, 'name': ['!=', self.name]})
		if existing:
			frappe.throw(f"Package with name '{self.package_name}' already exists")
	
	def before_save(self):
		# Ensure price is set
		if not self.price:
			self.price = 0