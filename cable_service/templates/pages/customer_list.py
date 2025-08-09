import frappe

def get_context(context):
    if frappe.session.user == "Guest":
        frappe.local.flags.redirect_location = "/login"
        raise frappe.Redirect
    
    context.customers = frappe.get_all('Customer Profile',
        fields=['name', 'customer_name', 'phone', 'city', 'service_status', 'payment_status', 'total_amount'],
        order_by='creation desc'
    )
    
    return context