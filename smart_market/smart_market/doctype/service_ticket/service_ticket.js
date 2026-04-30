// Copyright (c) 2026, dev_priyanshu dubey and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Service Ticket", {
frappe.ui.form.on('Service Ticket', {
    validate: function(frm) {
        let total = 0;
        (frm.doc.used_parts || []).forEach(d => {
            total += d.amount || 0;
        });
        frm.set_value('total_parts_cost', total);
    },
    priority: function(frm) {
        if(frm.doc.priority === "High") {
            frappe.msgprint("High Priority Service!");
        }
    },
    machine: function(frm) {
        if (frm.doc.machine) {
            frappe.db.get_doc('Machine', frm.doc.machine).then(doc => {
                let today = frappe.datetime.get_today();

                if (doc.warranty_expiry >= today) {
                    frappe.msgprint("Under Warranty ✅");
                } else {
                    frappe.msgprint("Out of Warranty ❌");
                }
            });
        }
    },
});
