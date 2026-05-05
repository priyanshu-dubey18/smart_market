# Copyright (c) 2026, dev_priyanshu dubey and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import timedelta
from frappe.utils import get_datetime

class Machine(Document):
    def validate(self):
        if self.purchase_date and self.machine_type:

            # 🔥 string → datetime convert
            purchase_date = get_datetime(self.purchase_date)

            mapping = {
                "Electrical": 1,
                "Mechanical": 2,
                "Hydraulic": 1,
                "CNC": 1,
                "Manual": 1.5
            }

            years = mapping.get(self.machine_type)

            if years:
                days = int(years * 365)

                # ✅ now सही calculation
                warranty_date = purchase_date + timedelta(days=days)

                # 🔥 फिर से string/date में set करो
                self.warranty_date = warranty_date.date()