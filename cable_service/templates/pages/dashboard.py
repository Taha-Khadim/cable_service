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
            context.stats['total_customers'] = frappe.db.count('Customer Profile') or 0
            context.stats['active_customers'] = frappe.db.count('Customer Profile', {'service_status': 'Active'}) or 0
            context.stats['pending_payments'] = frappe.db.count('Customer Profile', {'payment_status': 'Pending'}) or 0
            
            # Get total revenue from paid customers
            try:
                revenue_result = frappe.db.sql("""
                    SELECT COALESCE(SUM(CASE 
                        WHEN payment_status = 'Paid' THEN COALESCE(payment_amount, total_amount, 0)
                        ELSE 0 
                    END), 0) as total_revenue
                    FROM `tabCustomer Profile`
                """, as_dict=True)
                
                if revenue_result and len(revenue_result) > 0:
                    context.stats['total_revenue'] = float(revenue_result[0].get('total_revenue', 0))
            except Exception as revenue_error:
                frappe.log_error(f"Revenue calculation error: {str(revenue_error)}")
                context.stats['total_revenue'] = 0
            
            # Get recent customers
            try:
                context.recent_customers = frappe.get_all('Customer Profile',
                    fields=['name', 'customer_name', 'service_status', 'payment_status', 'creation'],
                    order_by='creation desc',
                    limit=5
                ) or []
            except Exception as customers_error:
                frappe.log_error(f"Recent customers error: {str(customers_error)}")
                context.recent_customers = []
            
    except Exception as e:
        frappe.log_error(f"Dashboard stats error: {str(e)}")
        context.needs_setup = True
    
    return context