import frappe

def get_context(context):
    if frappe.session.user == "Guest":
        frappe.local.flags.redirect_location = "/login"
        raise frappe.Redirect
    
    context.packages = frappe.get_all('Package',
        fields=['name', 'package_name', 'description', 'price', 'channels', 'is_active'],
        order_by='package_name'
    )
    
    return context