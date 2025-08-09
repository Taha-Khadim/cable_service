import frappe

def get_context(context):
	# Get all active packages for selection
	packages = frappe.get_all("Package", 
		filters={"is_active": 1}, 
		fields=["name", "package_name", "price", "description", "channels"]
	)
	context.packages = packages
	return context