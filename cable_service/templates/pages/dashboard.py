import frappe

def get_context(context):
    if frappe.session.user == "Guest":
        frappe.local.flags.redirect_location = "/login"
        raise frappe.Redirect
    
    # Get statistics
    context.stats = {
        'total_customers': frappe.db.count('Customer Profile'),
        'active_customers': frappe.db.count('Customer Profile', {'service_status': 'Active'}),
        'pending_payments': frappe.db.count('Customer Profile', {'payment_status': 'Pending'}),
        'total_revenue': frappe.db.sql("""
            SELECT COALESCE(SUM(payment_amount), 0) 
            FROM `tabCustomer Profile` 
            WHERE payment_status = 'Paid'
        """)[0][0] or 0
    }
    
    # Get recent customers
    context.recent_customers = frappe.get_all('Customer Profile',
        fields=['customer_name', 'service_status', 'payment_status'],
        order_by='creation desc',
        limit=5
    )
    
    return context