# Copyright (c) 2026, dev_priyanshu dubey and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import add_days

class ServiceTicket(Document):

    def after_insert(self):
        for item in self.used_parts:
            if item.part:

                machine = frappe.get_doc({
                    "doctype": "Machine",
                    "machine_name": item.item_name,
                    "customer": self.customer,
                    "purchase_date": self.creation,   # ya koi date field
                    "warranty_expiry": add_days(self.creation, 365),
                    "status": "Active"
                })

                machine.insert(ignore_permissions=True)

    def on_submit(self):
        if not self.sales_invoice:
            items = []

            for d in self.used_parts:
                items.append({
                    "item_code": d.part,
                    "qty": d.qty,
                    "rate": d.rate
                })

            invoice = frappe.get_doc({
                "doctype": "Sales Invoice",
                "customer": self.customer,
                "items": items
            })

            invoice.insert()
            invoice.submit()

            self.sales_invoice = invoice.name