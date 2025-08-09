import frappe

def get_context(context):
    if frappe.session.user == "Guest":
        frappe.local.flags.redirect_location = "/login"
        raise frappe.Redirect
    
    # Check if tables exist and get statistics safely
    try:
        context.stats = {
            'total_customers': frappe.db.count('Customer Profile') if frappe.db.table_exists('Customer Profile') else 0,
            'active_customers': frappe.db.count('Customer Profile', {'service_status': 'Active'}) if frappe.db.table_exists('Customer Profile') else 0,
            'pending_payments': frappe.db.count('Customer Profile', {'payment_status': 'Pending'}) if frappe.db.table_exists('Customer Profile') else 0,
            'total_revenue': 0
        }
        
        # Get total revenue safely
        if frappe.db.table_exists('Customer Profile'):
            revenue_result = frappe.db.sql("""
                SELECT COALESCE(SUM(payment_amount), 0) 
                FROM `tabCustomer Profile` 
                WHERE payment_status = 'Paid'
            """)
            context.stats['total_revenue'] = revenue_result[0][0] if revenue_result and revenue_result[0] else 0
    except Exception as e:
        frappe.log_error(f"Dashboard stats error: {str(e)}")
        context.stats = {
            'total_customers': 0,
            'active_customers': 0,
            'pending_payments': 0,
            'total_revenue': 0
        }
    
    # Get recent customers safely
    try:
        if frappe.db.table_exists('Customer Profile'):
            context.recent_customers = frappe.get_all('Customer Profile',
                fields=['customer_name', 'service_status', 'payment_status'],
                order_by='creation desc',
                limit=5
            )
        else:
            context.recent_customers = []
    except Exception as e:
        frappe.log_error(f"Recent customers error: {str(e)}")
        context.recent_customers = []
    
    # Check if setup is needed
    context.needs_setup = not frappe.db.table_exists('Customer Profile')
    
    return context