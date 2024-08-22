// // Copyright (c) 2024, ppcrc and contributors
// // For license information, please see license.txt

// frappe.ui.form.on("Student Attendance for Slow Learner", {
//     course_name:function(frm){
//         let course_name = frm.doc.course_name;
        
//         if(course_name){
//             frappe.call({
//                 method:"education_erp.api.get_student_list_course_enrollment",
//                 args:{course_name : course_name}
//             }).done((r) =>{
//                 console.log(r)
//                 frm.doc.slow_learner_students = [];

//                 $.each(r.message, function(_i,e){
//                     let entry = frm.add_child("slow_learner_students");
//                     entry.course_enrollment_id =e.name;
//                     entry.student_id = e.student;
//                     entry.student_name = e.student_name
//                 });
//                 refresh_field("slow_learner_students");
//             });
//         }
//     }
// });


frappe.ui.form.on("Student Attendance for Slow Learner", {
    course_name: function(frm) {
        let course_name = frm.doc.course_name;

        if (course_name) {
            frappe.call({
                method: "education_erp.api.get_student_list_course_enrollment",
                args: { course_name: course_name }
            }).done((r) => {
                console.log(r);
                frm.doc.slow_learner_students = [];

                $.each(r.message, function(_i, e) {
                    let entry = frm.add_child("slow_learner_students");
                    entry.course_enrollment_id = e.name;
                    entry.student_id = e.student;
                    entry.student_name = e.student_name;
                });
                refresh_field("slow_learner_students");
            });
        } else {
            // Clear the table if course_name is empty
            frm.clear_table("slow_learner_students");
            refresh_field("slow_learner_students");
        }
    }
});
