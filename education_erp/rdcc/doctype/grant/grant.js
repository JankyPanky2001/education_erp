frappe.ui.form.on('Grant', {
    onload: function(frm) {
        console.log("running.........");
        if (frm.is_new()) {
            frm.set_intro('Create New IPR');
        }
    },
    on_submit: function(frm) {
        frm.set_value('status', 'Pending');
        frm.save_or_update();
    },
    refresh: function(frm) {
        // Remove existing custom buttons
        frm.remove_custom_button(__('Approve'));
        frm.remove_custom_button(__('Reject'));

        // Check if the document status is 'Pending'
        if (frm.doc.status === 'Pending') {
            // Call get_instructor_program_details to get the necessary details
            frappe.call({
                method: "education_erp.rdcc.doctype.grant.grant.get_instructor_program_details",
                callback: function(response) {
                    if (response.message) {
                        console.log("response: ", response.message);
                        console.log("current user: ", frappe.session.user);

                        // Check if the current user matches the head of department or portfolio coordinator
                        let userIsAuthorized = response.message.some(item => 
                            frappe.session.user === item.custom_head_of_department_user_id || 
                            frappe.session.user === item.custom_portfolio_coordinator_user_id
                        );

                        // If the user is authorized, add Approve and Reject buttons
                        if (userIsAuthorized) {
                            frm.add_custom_button(__('Approve'), function() { 
                                frm.call('approve').then(() => {
                                    frappe.msgprint(`${frm.doc.employee_id}-${frm.doc.instructor} ${frm.doc.grant} Approved`);
                                    frm.reload_doc();                                   
                                    frm.save();
                                });
                            }, __("Action"));
                            
                            frm.add_custom_button(__('Reject'), function() {
                                frm.call('reject').then(() => {
                                    frappe.msgprint(`${frm.doc.employee_id}-${frm.doc.instructor} ${frm.doc.grant} Rejected`);
                                    frm.reload_doc();                                    
                                    frm.save();
                                });
                            }, __("Action"));
                        }
                    }
                }
            });
        }
    },
    start_date: function(frm) {
        calculate_duration(frm);
    },
    end_date: function(frm) {
        calculate_duration(frm);
    }
});

function calculate_duration(frm) {
    if (frm.doc.start_date && frm.doc.end_date) {
        // Convert the dates to moment objects for calculation
        let start_date = moment(frm.doc.start_date);
        let end_date = moment(frm.doc.end_date);

        // Check if start_date and end_date are in the same month and year
        if (start_date.year() === end_date.year() && start_date.month() === end_date.month()) {
            // Calculate the duration in days
            let days = end_date.diff(start_date, 'days');
            // Set the duration value in the format "{days} Days"
            let duration_of_the_project = `${days} Days`;
            frm.set_value('duration_of_the_project', duration_of_the_project);
        } else {
            // Calculate the total duration in months
            let total_months = end_date.diff(start_date, 'months');

            // Calculate the number of years and remaining months
            let years = Math.floor(total_months / 12);
            let months = total_months % 12;

            // Set the duration value in the format "{no_ofYear} Year(s) {no_of_months} Month(s)"
            let duration_of_the_project = `${years} Years ${months} Months`;
            frm.set_value('duration_of_the_project', duration_of_the_project);
        }
    }
}