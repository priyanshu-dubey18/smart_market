# Copyright (c) 2026, dev_priyanshu dubey and contributors
# For license information, please see license.txt

import frappe
from frappe import _

@frappe.whitelist(allow_guest=True)
def create_service_ticket(customer_name, machine_name, issue_description):
	"""Create a service ticket from frontend form"""

	try:
		# Validate required fields
		if not customer_name or not machine_name or not issue_description:
			frappe.throw(_("All fields are required"))

		# Check if customer exists, if not create one
		customer = frappe.db.exists("Customer", {"customer_name": customer_name})
		if not customer:
			customer_doc = frappe.get_doc({
				"doctype": "Customer",
				"customer_name": customer_name,
				"customer_type": "Individual"
			})
			customer_doc.insert(ignore_permissions=True)
			customer = customer_doc.name

		# Check if machine exists, if not create one
		machine = frappe.db.exists("Machine", {"machine_name": machine_name})
		if not machine:
			machine_doc = frappe.get_doc({
				"doctype": "Machine",
				"machine_name": machine_name,
				"customer": customer,
				"status": "Active"
			})
			machine_doc.insert(ignore_permissions=True)
			machine = machine_doc.name

		# Create service ticket
		service_ticket = frappe.get_doc({
			"doctype": "Service Ticket",
			"customer": customer,
			"machine": machine,
			"issue_description": issue_description,
			"status": "Open",
			"priority": "Medium"
		})

		service_ticket.insert(ignore_permissions=True)

		return {
			"success": True,
			"message": _("Service ticket created successfully"),
			"ticket_id": service_ticket.name
		}

	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "Service Ticket Creation Error")
		return {
			"success": False,
			"message": str(e)
		}