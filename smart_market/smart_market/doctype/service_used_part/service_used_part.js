// Copyright (c) 2026, dev_priyanshu dubey and contributors
// For license information, please see license.txt

frappe.ui.form.on('Service Used Part', {
    qty: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        row.amount = row.qty * row.rate;
        frm.refresh_field('used_parts');
    },
    rate: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        row.amount = row.qty * row.rate;
        frm.refresh_field('used_parts');
    },
    part: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        if (row.part) {
            frappe.db.get_value('Machine Part', row.part, 'price', (r) => {
                row.rate = r.price || 0;
                row.amount = (row.qty || 0) * row.rate;
                frm.refresh_field('used_parts');
            });
        }
    }
});