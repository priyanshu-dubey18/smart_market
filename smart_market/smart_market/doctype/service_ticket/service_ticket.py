import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt, getdate, nowdate

class ServiceTicket(Document):
	def validate(self):
		self.set_warranty_and_service_type()
		self.calculate_totals()

	def set_warranty_and_service_type(self):
		if not self.machine:
			return

		warranty_date = frappe.db.get_value("Machine", self.machine, "warranty_date")
		under_warranty = bool(warranty_date and getdate(warranty_date) >= getdate(nowdate()))

		self.warranty_status = "Under Warranty" if under_warranty else "Out of Warranty"
		self.service_type = "Free" if under_warranty else "Paid"

	def calculate_totals(self):
		total_parts_cost = 0

		for row in self.used_parts:
			row.qty = flt(row.qty)
			row.rate = flt(row.rate)
			row.amount = row.qty * row.rate
			total_parts_cost += row.amount

		self.total_parts_cost = total_parts_cost
		self.total_cost = 0 if self.warranty_status == "Under Warranty" else total_parts_cost

	def on_submit(self):
		self.set_warranty_and_service_type()
		self.calculate_totals()

		# Create invoice immediately if warranty has expired
		self.create_invoice_if_warranty_expired()

	def create_sales_invoice(self):
		if not self.customer:
			frappe.throw(_("Customer is required to create Sales Invoice."))

		items = self.get_invoice_items()
		if not items:
			frappe.throw(_("Add at least one used part with an Item to create Sales Invoice."))

		invoice = frappe.get_doc({
			"doctype": "Sales Invoice",
			"customer": self.customer,
			"items": items,
		})
		invoice.insert(ignore_permissions=True)
		invoice.submit()

		return invoice

	def create_invoice_if_warranty_expired(self):
		"""Create sales invoice if warranty has expired and no invoice exists"""
		if self.sales_invoice:
			return  # Already has invoice

		if self.status != "Completed":
			return  # Not completed

		if not self.machine:
			return

		warranty_date = frappe.db.get_value("Machine", self.machine, "warranty_date")
		if not warranty_date:
			return  # No warranty date, assume out of warranty

		if getdate(warranty_date) >= getdate(nowdate()):
			return  # Still under warranty

		# Warranty expired, create invoice
		try:
			invoice = self.create_sales_invoice()
			self.db_set("sales_invoice", invoice.name, update_modified=False)
			frappe.db.commit()
		except Exception as e:
			frappe.log_error(f"Failed to create invoice for Service Ticket {self.name}: {str(e)}")
