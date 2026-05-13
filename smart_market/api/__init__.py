import frappe
from frappe import _
from frappe.utils import getdate, nowdate


@frappe.whitelist(allow_guest=True)
def create_service_ticket(customer_name, machine_name, serial_number, issue_description):
	"""Create a draft service ticket from the public frontend form."""

	try:
		if not customer_name or not machine_name or not serial_number or not issue_description:
			frappe.throw(_("All fields are required"))

		customer_name = customer_name.strip()
		machine_name = machine_name.strip()
		serial_number = serial_number.strip()
		issue_description = issue_description.strip()

		customer = frappe.db.exists("Customer", {"customer_name": customer_name})
		if not customer:
			customer_doc = frappe.get_doc({
				"doctype": "Customer",
				"customer_name": customer_name,
				"customer_type": "Individual",
			})
			customer_doc.insert(ignore_permissions=True)
			customer = customer_doc.name

		machine = frappe.db.exists("Machine", {"serial__number": serial_number})
		if not machine:
			machine_doc = frappe.get_doc({
				"doctype": "Machine",
				"machine_name": machine_name,
				"serial__number": serial_number,
				"customer": customer,
				"status": "Active",
			})
			machine_doc.insert(ignore_permissions=True)
			machine = machine_doc.name
		else:
			machine_doc = frappe.get_doc("Machine", machine)

		warranty_date = machine_doc.get("warranty_date")
		under_warranty = bool(warranty_date and getdate(warranty_date) >= getdate(nowdate()))

		service_ticket = frappe.get_doc({
			"doctype": "Service Ticket",
			"customer": customer,
			"machine": machine,
			"issue_description": issue_description,
			"status": "Open",
			"priority": "Medium",
			"warranty_status": "Under Warranty" if under_warranty else "Out of Warranty",
			"service_type": "Free" if under_warranty else "Paid",
		})
		service_ticket.insert(ignore_permissions=True)
		frappe.db.commit()

		return {
			"success": True,
			"message": _("Service ticket created successfully"),
			"ticket_id": service_ticket.name,
			"customer": customer,
			"machine": machine,
			"service_type": service_ticket.service_type,
			"warranty_status": service_ticket.warranty_status,
		}

	except frappe.ValidationError as e:
		frappe.log_error(frappe.get_traceback(), "Service Ticket Validation Error")
		return {
			"success": False,
			"message": str(e),
		}
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "Service Ticket Creation Error")
		return {
			"success": False,
			"message": str(e),
		}
