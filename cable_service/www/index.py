import frappe

def get_context(context):
    context.packages = frappe.get_all('Package',
        filters={'is_active': 1},
        fields=['package_name', 'price', 'description', 'channels'],
        limit=4
    )
    return context