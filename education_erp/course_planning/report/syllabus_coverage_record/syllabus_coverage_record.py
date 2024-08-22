
import frappe
from frappe import _, msgprint

def execute(filters=None):
    if not filters:
        filters = {}
    if filters.get('date'):
        start_date = filters['date'][0]
        end_date = filters['date'][1]
        filters['date'] = ["between", (start_date, end_date)]
    
    data, columns = [], []
    
    columns = get_columns()
    cs_data = get_cs_data(filters)
    
    if not cs_data:
        msgprint(_('No Records Found'))
        return columns, cs_data, None, None, None
    
    data = []
    for d in cs_data:
        row = frappe._dict({
            'program':d.program,
            'department_name':d.department_name,
            'academic_year': d.academic_year,
            'academic_term':d.academic_term,
            'course_name':d.course_name,
            'date':d.date,
            'class_or_division':d.class_or_division,
            'course_code':d.course_code,
            'teaching_scheme':d.teaching_scheme,
            'batch':d.batch,
            'period':d.period,
            'faculty_name':d.faculty_name,
            'no_of_thpr_planned':d.no_of_thpr_planned,
            'no_of_thpr_taken':d.no_of_thpr_taken,
            '_syllabus_covered':d._syllabus_covered
            
        })
        data.append(row)
        
    return columns, data, None, None, None

def get_columns():
    return [
        {
            "fieldname": "department_name",
            "label": _("Department"),
            "fieldtype": "Link",
            "options": "Department",
            'width': '120'
        },
		{
            "fieldname": "program",
            "label": _("Select Program"),
            "fieldtype": "Link",
            "options": "Program",
            'width': '120'
        },
		{
            "fieldname": "academic_year",
            "label": _("Academic Year"),
            "fieldtype": "Link",
            "options": "Academic Year",
            'width': '120'
        },
		{
            "fieldname": "academic_term",
            "label": _("Academic Term"),
            "fieldtype": "Link",
            "options": "Academic Term",
            'width': '120'
        },
		{
            "fieldname": "class_or_division",
            "label": _("Class"),
            "fieldtype": "Data",
            'width': '120'
        },  
		{
            "fieldname": "course_name",
            "label": _("Course"),
            "fieldtype": "Link",
            "options": "Course",
            'width': '120'
        },
  		{
            "fieldname": "course_code",
            "label": _("Course Code"),
            "fieldtype": "Data",
            'width': '120'
        },
  		{
            "fieldname": "teaching_scheme",
            "label": _("Teaching Scheme"),
            "fieldtype": "Data",
            'width': '120'
        },
  		{
            "fieldname": "batch",
            "label": _("Batch"),
            "fieldtype": "Data",
            'width': '120'
        },
  		{
            "fieldname": "period",
            "label": _("period"),
            "fieldtype": "Data",
            'width': '120'
        },             
		{
            "fieldname": "date",
            "label": _("Date"),
            "fieldtype": "Date",
            'width': '120',
        },
		{
            "fieldname": "faculty_name",
            "label": _("faculty_name"),
            "fieldtype": "Link",
			"options": "Instructor",
            'width': '120'
        },
  		{
            "fieldname": "no_of_thpr_planned",
            "label": _("No. of TH/PR planned"),
            "fieldtype": "Data",
            'width': '120'
        },
      	{
            "fieldname": "no_of_thpr_taken",
            "label": _("No. of TH/PR taken"),
            "fieldtype": "Data",
            'width': '120'
        }          
    ]

def get_cs_data(filters):
    conditions = get_conditions(filters)
    data = frappe.get_all(
        doctype='Syllabus Coverage Record',
        fields=[
            'department_name', 'program', 'academic_year', 'academic_term', 'class_or_division', 'course_name', 
            'course_code', 'teaching_scheme', 'batch', 'date', 'period', 'faculty_name', 'no_of_thpr_planned', 'no_of_thpr_taken', '_syllabus_covered'
        ],
        filters=conditions
    )
    return data

def get_conditions(filters):
    conditions = {}
    for key, value in filters.items():
        if filters.get(key):
            conditions[key] = value
    return conditions