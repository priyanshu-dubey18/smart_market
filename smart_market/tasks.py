# Scheduled tasks for smart_market

import frappe
from frappe.utils import nowdate

def daily():
	"""Run daily tasks"""
	create_invoices_for_expired_warranties()

def create_invoices_for_expired_warranties():
	"""Create sales invoices for completed service tickets where warranty has expired"""
	try:
		# Get all completed service tickets without sales invoice
		tickets = frappe.get_all(
			"Service Ticket",
			filters={
				"status": "Completed",
				"sales_invoice": ["is", "not set"],
				"docstatus": 1  # Submitted
			},
			fields=["name", "machine"]
		)

		for ticket_data in tickets:
			ticket = frappe.get_doc("Service Ticket", ticket_data.name)
			ticket.create_invoice_if_warranty_expired()

		frappe.db.commit()

	except Exception as e:
		frappe.log_error(f"Error in create_invoices_for_expired_warranties: {str(e)}")