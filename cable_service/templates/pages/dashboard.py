import frappe

def get_context(context):
    if frappe.session.user == "Guest":
        frappe.local.flags.redirect_location = "/login"
        raise frappe.Redirect
    
    # Initialize default stats
    context.stats = {
        'total_customers': 0,
        'active_customers': 0,
        'pending_payments': 0,
        'total_revenue': 0
    }
    
    context.recent_customers = []
    context.needs_setup = True
    
    # Check if tables exist and get statistics safely
    try:
        if frappe.db.table_exists('Customer Profile'):
            context.needs_setup = False
            
            # Get customer counts
            context.stats['total_customers'] = frappe.db.count('Customer Profile')
            context.stats['active_customers'] = frappe.db.count('Customer Profile', {'service_status': 'Active'})
            context.stats['pending_payments'] = frappe.db.count('Customer Profile', {'payment_status': 'Pending'})
            
            # Get total revenue from paid customers
            revenue_result = frappe.db.sql("""
                SELECT COALESCE(SUM(CASE 
                    WHEN payment_status = 'Paid' THEN COALESCE(payment_amount, total_amount, 0)
                    ELSE 0 
                END), 0) as total_revenue
                FROM `tabCustomer Profile`
            """, as_dict=True)
            
            if revenue_result and len(revenue_result) > 0:
                context.stats['total_revenue'] = float(revenue_result[0].get('total_revenue', 0))
            
            # Get recent customers
            context.recent_customers = frappe.get_all('Customer Profile',
                fields=['name', 'customer_name', 'service_status', 'payment_status', 'creation'],
                order_by='creation desc',
                limit=5
            )
            
    except Exception as e:
        frappe.log_error(f"Dashboard stats error: {str(e)}")
        # Keep default values on error
        pass
    
    return context