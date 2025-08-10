import frappe

def get_context(context):
    if frappe.session.user == "Guest":
        frappe.local.flags.redirect_location = "/login"
        raise frappe.Redirect
    
    # Get customer ID from URL
    customer_id = frappe.form_dict.get('customer_id')
    
    if not customer_id:
        context.customer = None
        return context
    
    try:
        # Get customer details with packages
        customer = frappe.get_doc('Customer Profile', customer_id)
        context.customer = customer
    except frappe.DoesNotExistError:
        context.customer = None
    except Exception as e:
        frappe.log_error(f"User profile error: {str(e)}")
        context.customer = None
    
    return context