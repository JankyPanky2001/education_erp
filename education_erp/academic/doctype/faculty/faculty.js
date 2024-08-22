// Copyright (c) 2024, ppcrc and contributors
// For license information, please see license.txt

frappe.ui.form.on("Course ceo and co", {
    onload: function(frm) {
        frappe.call({
            method: 'frappe.client.get',
            args: {
                doctype: 'Employee',
                filters: { 'user_id': frappe.session.user }
            },
            callback: function(r) {
                if (r.message) {
                    frm.set_value('department', r.message.department);
                    frm.set_value('program', r.message.custom_program);
                    frm.set_value('faculty_name', r.message.employee_name);
                } else {
                    frappe.msgprint(__('No Employee record found for the current user.'));
                }
            },
            error: function(err) {
                frappe.msgprint(__('An error occurred while fetching the Employee record.'));
                console.error(err);
            }
        });
    }
});
