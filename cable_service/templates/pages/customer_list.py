import frappe

def get_context(context):
    if frappe.session.user == "Guest":
        frappe.local.flags.redirect_location = "/login"
        raise frappe.Redirect
    
    # Check if table exists before querying
    try:
        if frappe.db.table_exists('Customer Profile'):
            context.customers = frappe.get_all('Customer Profile',
                fields=['name', 'customer_name', 'phone', 'city', 'service_status', 'payment_status', 'total_amount'],
                order_by='creation desc'
            )
        else:
            context.customers = []
            context.needs_setup = True
    except Exception as e:
        frappe.log_error(f"Customer list error: {str(e)}")
        context.customers = []
        context.needs_setup = True
    
    return context