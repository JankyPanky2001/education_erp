frappe.ui.form.on("Theory Lesson Plan", {
    course:function(frm){
        let course = frm.doc.course;
        
        if(course){
            frappe.call({
                method:"education_erp.api.get_unit_theory_lesson_plan",
                args: {course : course}
            }).done((r) =>{
                frm.doc.unit =[];

                $.each(r.message,function(_i,e){
                    let entry = frm.add_child("unit");
                    entry.unit_title = e.name;
                    entry.unit_number = e.unit_number;
                });
                refresh_field("unit");
                
            });
            
        }else {
            // Clear the table if course_name is empty
            frm.clear_table("unit");
            refresh_field("unit");
        }
    }
});
