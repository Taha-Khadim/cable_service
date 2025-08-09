import frappe
from frappe.model.document import Document

class Package(Document):
	def validate(self):
		if self.price < 0:
			frappe.throw("Price cannot be negative")