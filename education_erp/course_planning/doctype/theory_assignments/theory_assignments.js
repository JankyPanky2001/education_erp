// Copyright (c) 2024, ppcrc and contributors
// For license information, please see license.txt

frappe.ui.form.on("Theory Assignments", {
	refresh(frm) {
        frm.set_query('unit_name', function (doc) {
            return { filters: { course: doc.course_name } };
        });

	},
});
