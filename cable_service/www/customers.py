import frappe

def get_context(context):
    if frappe.session.user == "Guest":
        frappe.local.flags.redirect_location = "/login"
        raise frappe.Redirect
    
    # Initialize default values
    context.customers = []
    context.needs_setup = True
    
    # Check if tables exist and get customers safely
    try:
        if frappe.db.table_exists('Customer Profile'):
            context.needs_setup = False
            context.customers = frappe.get_all('Customer Profile',
                fields=[
                    'name', 'customer_name', 'phone', 'email', 'address', 'city', 
                    'service_status', 'payment_status', 'total_amount', 'payment_amount',
                    'creation'
                ],
                order_by='creation desc'
            ) or []
    except Exception as e:
        frappe.log_error(f"Customers page error: {str(e)}")
        context.needs_setup = True
    
    return context