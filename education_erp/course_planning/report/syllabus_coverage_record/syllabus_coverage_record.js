// Copyright (c) 2024, ppcrc and contributors
// For license information, please see license.txt

frappe.query_reports["Syllabus Coverage Record"] = {
	"filters": [
		{
            "fieldname": "program",
            "label": __("Select Program"),
            "fieldtype": "Link",
            "options": "Program"
        },
		{
            "fieldname": "department_name",
            "label": __("Department"),
            "fieldtype": "Link",
            "options": "Department"
        },
		{
            "fieldname": "academic_year",
            "label": __("Academic Year"),
            "fieldtype": "Link",
            "options": "Academic Year"
        },
		{
            "fieldname": "academic_term",
            "label": __("Academic Term"),
            "fieldtype": "Link",
            "options": "Academic Term"
        },
		{
            "fieldname": "course_name",
            "label": __("Course"),
            "fieldtype": "Link",
            "options": "Course"
        },
		{
            "fieldname": "date",
            "label": __("Date"),
            "fieldtype": "DateRange"
        },
		{
            "fieldname": "faculty_name",
            "label": __("Faculty Name"),
            "fieldtype": "Link",
			"options": "Instructor"
        },

	]
};
