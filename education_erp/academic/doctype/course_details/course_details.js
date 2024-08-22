frappe.ui.form.on('Course Details', {
    course_name: function(frm) {
        let course_name = frm.doc.course_name;

        if (course_name) {
            // Fetch unit list
            frappe.call({
                method: "education_erp.api.get_unit_list",
                args: { course_name: course_name }
            }).done((r) => {
                frm.doc.course_unit_detail = [];

                $.each(r.message, function(_i, e) {
                    let entry = frm.add_child("course_unit_detail");
                    entry.unit_title = e.name;
                    entry.unit_number = e.unit_number;
                });
                refresh_field("course_unit_detail");
            });

            // Fetch practical list 
            frappe.call({
                method: "education_erp.api.get_pratical_list",  // Ensure the method name is correct
                args: { course_name: course_name }
            }).done((response) => {
                frm.doc.practical_detail = [];

                $.each(response.message, function(_i, e) {
                    let entry = frm.add_child("practical_detail");
                    entry.practical_id = e.name;
                    entry.practical_title = e.experiment__assignment_title;
                });
                refresh_field("practical_detail");
            });

            // Fetch tutorial list
            frappe.call({
                method: "education_erp.api.get_tutorial_list",  // Ensure the method name is correct
                args: { course_name: course_name }
            }).done((tutorial_response) => {
                frm.doc.tutorial_detail = [];

                // Ensure you're iterating over tutorial_response.message
                $.each(tutorial_response.message, function(_i, e) {
                    let entry = frm.add_child("tutorial_detail");

                    entry.tutorial_id = e.name;
                    entry.tutorial_name = e.tutorial_title;
                    entry.planned_date = e.planned_date;
                    entry.tutorial_number=e.tutorial_no;
                    entry.execution_date = e.execution_date;
                });

                refresh_field("tutorial_detail");
            });
        }
    }
});


