import frappe

@frappe.whitelist()
def get_unit_list(course_name):
    units = frappe.db.sql(f""" SELECT name,unit_number   FROM   `tabUnit` WHERE course ='{course_name}' """, as_dict =True)
    return units


@frappe.whitelist()
def get_pratical_list(course_name):
    pratical = frappe.db.sql(f""" SELECT name,experiment__assignment_title   FROM   `tabPractical Plan` WHERE course_name ='{course_name}' """, as_dict =True)
    return pratical


@frappe.whitelist()
def get_tutorial_list(course_name):
    tutorial = frappe.db.sql(f""" SELECT name,tutorial_title,tutorial_no,planned_date,execution_date   FROM   `tabTutorial  Plan` WHERE course_name ='{course_name}' """, as_dict =True)
    return tutorial


@frappe.whitelist()
def get_unit_theory_lesson_plan(course):
    unit_theory_lesson_plan = frappe.db.sql(f""" SELECT name,unit_number     FROM   `tabUnit` WHERE course ='{course}' """, as_dict =True)
    return unit_theory_lesson_plan

@frappe.whitelist()
def get_student_list_course_enrollment(course_name):
    student_list_course_enrollment = frappe.db.sql(f""" SELECT name,student,student_name     FROM   `tabCourse Enrollment` WHERE course ='{course_name}' """, as_dict =True)
    return student_list_course_enrollment


