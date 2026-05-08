# Copyright (c) 2026, dev_priyanshu dubey and contributors
# For license information, please see license.txt

import frappe
from frappe import _

@frappe.whitelist(allow_guest=True)
def create_service_ticket(customer_name, machine_name, serial_number, issue_description):
	"""Create a service ticket from frontend form"""

	try:
		# Validate required fields
		if not customer_name or not machine_name or not serial_number or not issue_description:
			frappe.throw(_("All fields are required"))

		# Check if customer exists, if not create one
		customer = frappe.db.exists("Customer", {"customer_name": customer_name})
		if not customer:
			try:
				customer_doc = frappe.get_doc({
					"doctype": "Customer",
					"customer_name": customer_name,
					"customer_type": "Individual"
				})
				customer_doc.insert(ignore_permissions=True)
				customer = customer_doc.name
			except Exception as e:
				frappe.log_error(f"Customer creation error: {str(e)}", "Service Ticket API")
				customer = customer_name  # Use the name directly

		# Check if machine exists, if not create one
		machine = frappe.db.exists("Machine", {"serial__number": serial_number})
		if not machine:
			try:
				machine_doc = frappe.get_doc({
					"doctype": "Machine",
					"machine_name": machine_name,
					"serial__number": serial_number,
					"customer": customer,
					"status": "Active"
				})
				machine_doc.insert(ignore_permissions=True)
				machine = machine_doc.name
			except Exception as e:
				frappe.log_error(f"Machine creation error: {str(e)}", "Service Ticket API")
				machine = serial_number  # Use serial number as fallback

		# Create and submit service ticket
		service_ticket = frappe.get_doc({
			"doctype": "Service Ticket",
			"customer": customer,
			"machine": machine,
			"issue_description": issue_description,
			"status": "Open",
			"priority": "Medium"
		})

		service_ticket.insert(ignore_permissions=True)
		service_ticket.submit()

		frappe.db.commit()

		return {
			"success": True,
			"message": _("Service ticket created successfully"),
			"ticket_id": service_ticket.name
		}

	except frappe.ValidationError as e:
		frappe.log_error(frappe.get_traceback(), "Service Ticket Validation Error")
		return {
			"success": False,
			"message": str(e)
		}
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "Service Ticket Creation Error")
		return {
			"success": False,
			"message": str(e)
		}
