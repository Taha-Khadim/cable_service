import frappe
from frappe import _
import json

@frappe.whitelist()
def create_customer(data):
    """Create a new customer with packages"""
    try:
        if isinstance(data, str):
            data = json.loads(data)
        
        # Create customer profile
        customer_doc = frappe.new_doc("Customer Profile")
        customer_doc.customer_name = data.get('customer_name')
        customer_doc.phone = data.get('phone')
        customer_doc.email = data.get('email')
        customer_doc.cnic = data.get('cnic')
        customer_doc.city = data.get('city')
        customer_doc.address = data.get('address')
        customer_doc.payment_amount = float(data.get('payment_amount', 0))
        customer_doc.payment_mode = data.get('payment_mode', 'Cash')
        customer_doc.payment_status = data.get('payment_status', 'Pending')
        customer_doc.payment_date = data.get('payment_date')
        customer_doc.created_by = frappe.session.user
        
        # Add selected packages
        selected_packages = data.get('selected_packages', [])
        total_amount = 0
        
        for package_data in selected_packages:
            package_row = customer_doc.append('selected_packages')
            package_row.package = package_data.get('package')
            package_row.package_name = package_data.get('package_name')
            package_row.price = float(package_data.get('price', 0))
            total_amount += package_row.price
        
        customer_doc.total_amount = total_amount
        
        # Set service status based on payment
        if customer_doc.payment_status == 'Paid':
            customer_doc.service_status = 'Active'
        else:
            customer_doc.service_status = 'Pending'
        
        customer_doc.insert()
        frappe.db.commit()
        
        return {
            'success': True,
            'message': 'Customer created successfully',
            'customer_id': customer_doc.name
        }
        
    except Exception as e:
        frappe.log_error(f"Customer creation error: {str(e)}")
        return {
            'success': False,
            'message': str(e)
        }

@frappe.whitelist()
def get_packages():
    """Get all active packages"""
    try:
        packages = frappe.get_all('Package',
            filters={'is_active': 1},
            fields=['name', 'package_name', 'description', 'price', 'channels'],
            order_by='package_name'
        )
        return {
            'success': True,
            'packages': packages
        }
    except Exception as e:
        frappe.log_error(f"Get packages error: {str(e)}")
        return {
            'success': False,
            'message': str(e),
            'packages': []
        }

@frappe.whitelist()
def update_customer_payment(customer_id, payment_data):
    """Update customer payment information"""
    try:
        if isinstance(payment_data, str):
            payment_data = json.loads(payment_data)
        
        customer = frappe.get_doc('Customer Profile', customer_id)
        customer.payment_amount = float(payment_data.get('payment_amount', 0))
        customer.payment_mode = payment_data.get('payment_mode')
        customer.payment_status = payment_data.get('payment_status')
        customer.payment_date = payment_data.get('payment_date')
        
        # Update service status based on payment
        if customer.payment_status == 'Paid':
            customer.service_status = 'Active'
        elif customer.payment_status == 'Pending':
            customer.service_status = 'Pending'
        else:
            customer.service_status = 'Inactive'
        
        customer.save()
        frappe.db.commit()
        
        return {
            'success': True,
            'message': 'Payment updated successfully'
        }
        
    except Exception as e:
        frappe.log_error(f"Payment update error: {str(e)}")
        return {
            'success': False,
            'message': str(e)
        }

@frappe.whitelist()
def update_service_status(customer_id, service_status):
    """Update customer service status"""
    try:
        customer = frappe.get_doc('Customer Profile', customer_id)
        customer.service_status = service_status
        customer.save()
        frappe.db.commit()
        
        return {
            'success': True,
            'message': 'Service status updated successfully'
        }
        
    except Exception as e:
        frappe.log_error(f"Service status update error: {str(e)}")
        return {
            'success': False,
            'message': str(e)
        }