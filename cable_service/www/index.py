import frappe

def get_context(context):
    try:
        if frappe.db.table_exists('Package'):
            context.packages = frappe.get_all('Package',
                filters={'is_active': 1},
                fields=['package_name', 'price', 'description', 'channels'],
                limit=4
            )
        else:
            context.packages = []
    except Exception as e:
        frappe.log_error(f"Index packages error: {str(e)}")
        context.packages = []
    
    return context