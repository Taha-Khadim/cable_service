import frappe
from frappe import _
import json

@frappe.whitelist()
def create_package(data):
    """Create a new package"""
    try:
        if isinstance(data, str):
            data = json.loads(data)
        
        # Check if package name already exists
        if frappe.db.exists('Package', data.get('package_name')):
            return {
                'success': False,
                'message': 'Package with this name already exists'
            }
        
        package_doc = frappe.new_doc("Package")
        package_doc.package_name = data.get('package_name')
        package_doc.description = data.get('description', '')
        package_doc.price = float(data.get('price', 0))
        package_doc.channels = data.get('channels', '')
        package_doc.is_active = int(data.get('is_active', 1))
        
        package_doc.insert()
        frappe.db.commit()
        
        return {
            'success': True,
            'message': 'Package created successfully',
            'package_id': package_doc.name
        }
        
    except Exception as e:
        frappe.log_error(f"Package creation error: {str(e)}")
        return {
            'success': False,
            'message': str(e)
        }

@frappe.whitelist()
def update_package(package_id, data):
    """Update an existing package"""
    try:
        if isinstance(data, str):
            data = json.loads(data)
        
        package_doc = frappe.get_doc("Package", package_id)
        package_doc.package_name = data.get('package_name')
        package_doc.description = data.get('description', '')
        package_doc.price = float(data.get('price', 0))
        package_doc.channels = data.get('channels', '')
        package_doc.is_active = int(data.get('is_active', 1))
        
        package_doc.save()
        frappe.db.commit()
        
        return {
            'success': True,
            'message': 'Package updated successfully'
        }
        
    except Exception as e:
        frappe.log_error(f"Package update error: {str(e)}")
        return {
            'success': False,
            'message': str(e)
        }

@frappe.whitelist()
def toggle_package_status(package_id, is_active):
    """Toggle package active status"""
    try:
        package_doc = frappe.get_doc("Package", package_id)
        package_doc.is_active = int(is_active)
        package_doc.save()
        frappe.db.commit()
        
        status = 'activated' if is_active else 'deactivated'
        return {
            'success': True,
            'message': f'Package {status} successfully'
        }
        
    except Exception as e:
        frappe.log_error(f"Package toggle error: {str(e)}")
        return {
            'success': False,
            'message': str(e)
        }

@frappe.whitelist()
def get_package_details(package_id):
    """Get package details"""
    try:
        package = frappe.get_doc('Package', package_id)
        return {
            'success': True,
            'package': {
                'name': package.name,
                'package_name': package.package_name,
                'description': package.description,
                'price': package.price,
                'channels': package.channels,
                'is_active': package.is_active
            }
        }
    except Exception as e:
        frappe.log_error(f"Get package details error: {str(e)}")
        return {
            'success': False,
            'message': str(e)
        }