// Copyright (c) 2024, ppcrc and contributors
// For license information, please see license.txt

frappe.ui.form.on("Elective Subject", {
	refresh(frm) {

        frm.set_query('electives_opted', function (doc) {
            return { filters: { department: doc.department_name, custom_elective:1 } };
        });

	},
});
