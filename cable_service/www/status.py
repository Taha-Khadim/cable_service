import frappe

def get_context(context):
    if frappe.session.user == "Guest":
        frappe.local.flags.redirect_location = "/login"
        raise frappe.Redirect
    
    # Initialize default values
    context.customers = []
    
    # Check if tables exist and get customers safely
    try:
        if frappe.db.table_exists('Customer Profile'):
            context.customers = frappe.get_all('Customer Profile',
                fields=[
                    'name', 'customer_name', 'phone', 'service_status', 
                    'payment_status', 'modified'
                ],
                order_by='modified desc'
            ) or []
    except Exception as e:
        frappe.log_error(f"Status page error: {str(e)}")
        context.customers = []
    
    return context