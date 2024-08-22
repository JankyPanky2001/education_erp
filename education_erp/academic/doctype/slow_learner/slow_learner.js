// Copyright (c) 2024, ppcrc and contributors
// For license information, please see license.txt

frappe.ui.form.on("Slow Learner", {
	refresh(frm) {
        frm.set_query('unit_covered', function (doc) {
            return { filters: { course: doc.course } };
        });

	},
});
