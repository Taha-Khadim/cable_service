import frappe

def get_context(context):
    if frappe.session.user == "Guest":
        frappe.local.flags.redirect_location = "/login"
        raise frappe.Redirect
    
    # Initialize default values
    context.packages = []
    context.needs_setup = True
    
    # Check if tables exist and get packages safely
    try:
        if frappe.db.table_exists('Package') and frappe.db.table_exists('Customer Profile'):
            context.needs_setup = False
            context.packages = frappe.get_all('Package',
                filters={'is_active': 1},
                fields=['name', 'package_name', 'description', 'price', 'channels'],
                order_by='package_name'
            ) or []
    except Exception as e:
        frappe.log_error(f"Add customer page error: {str(e)}")
        context.needs_setup = True
    
    return context