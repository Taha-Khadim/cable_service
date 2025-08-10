import frappe

def get_context(context):
    if frappe.session.user == "Guest":
        frappe.local.flags.redirect_location = "/login"
        raise frappe.Redirect
    
    # Check if table exists before querying
    try:
        if frappe.db.table_exists('Package'):
            context.packages = frappe.get_all('Package',
                fields=['name', 'package_name', 'description', 'price', 'channels', 'is_active'],
                order_by='package_name'
            )
            context.needs_setup = False
        else:
            context.packages = []
            context.needs_setup = True
    except Exception as e:
        frappe.log_error(f"Packages error: {str(e)}")
        context.packages = []
        context.needs_setup = True
    
    return context