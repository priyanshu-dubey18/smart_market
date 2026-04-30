# Copyright (c) 2026, dev_priyanshu dubey and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ServiceTicket(Document):
    def on_submit(self):
        for d in self.used_parts:
            if d.part and d.qty:

                part = frappe.get_doc("Machine Part", d.part)

                part.stock_qty = (part.stock_qty or 0) - d.qty

                part.save(ignore_permissions=True)