

import frappe
from frappe import _, msgprint

def execute(filters=None):
    associated_programs = get_associated_programs()
    if not filters:
        filters = {}

    if filters.get('date_of_publication'):
        start_date = filters['date_of_publication'][0]
        end_date = filters['date_of_publication'][1]
        filters['date_of_publication'] = ["between", (start_date, end_date)]

    data, columns = [], []
    columns = get_columns()  # Populate the columns list
    cs_data = get_cs_data(filters, associated_programs)

    if not cs_data:
        msgprint(_('No Records Found'))
        return columns, cs_data, None, None, None

    data = []
    for d in cs_data:
        row = frappe._dict({
            'publication': d.publication,
            'academic_year': d.academic_year,
            'date_of_publication': d.date_of_publication,
            'program': d.program,
            'instructor': d.instructor,
            'employee_id': d.employee_id,
            'title': d.title,
            'name_of_journal': d.name_of_journal,
            'name_of_the_conference': d.name_of_the_conference,
            'financial_year': d.financial_year,
            'place_of_publication': d.place_of_publication,
            'national_international': d.national_international,
            'affiliation': d.affiliation,
            'publisher': d.publisher,
            'is_ugc_care_listed_': d.is_ugc_care_listed_,
            'proof': d.proof,
            'page_numbers': d.page_numbers,
            'citation': d.citation,
            'volume': d.volume,
            'status': d.status,
            'impact_factor': d.impact_factor,
            'issn_isbn': d.issn_isbn,
            'linkdoi': d.linkdoi,
            'indexed': d.indexed,
            'attachment': d.attachment,
            'issue':d.issue
        })
        data.append(row)

    chart = get_chart_data(data)
    report_summary = get_report_summary(data, associated_programs)
        
    return columns, data, None, chart, report_summary



def get_associated_programs():
    current_user = frappe.session.user
    user_data = frappe.db.sql("""
        SELECT 
            e.custom_program,
            p.custom_head_of_department_user_id,
            p.custom_portfolio_coordinator_user_id
        FROM 
            tabEmployee e
        JOIN 
            tabProgram p
        ON 
            e.custom_program = p.program_name
        WHERE 
            e.user_id = %s
    """, (current_user,), as_dict=True)

    if not user_data:
        return []

    user_roles = user_data[0]
    if current_user in [user_roles.custom_head_of_department_user_id, user_roles.custom_portfolio_coordinator_user_id]:
        return [user_roles.custom_program]
    
    return []


def get_columns():
    return [
        {
            "fieldname": "publication",
            "label": _("Publication"),  # Ensure to use `_` here
            "fieldtype": "Link",
            "options": "Publication Type",
            'width': '120'
        },
        {
            "fieldname": "program",
            "label": _("Program"),
            "fieldtype": "Link",
            "options": "Program",
            'width': '170'
        },
        {
            "fieldname": "instructor",
            "label": _("Name of Authors"),
            "fieldtype": "Link",
            "options": "Instructor",
            'width': '170'
        },
        {
            "fieldname": "employee_id",
            "label": _("Employee ID"),
            "fieldtype": "Data",
            'width': '170'
        },
        {
            "fieldname": "academic_year",
            "label": _("Academic Year"),
            "fieldtype": "Link",
            "options": "Academic Year",
            'width': '120'
        },
        {
            "fieldname": "date_of_publication",
            "label": _("Date of Publication"),
            "fieldtype": "Date",
            'width': '120'
        },
        {
            "fieldname": "title",
            "label": _("Title"),
            "fieldtype": "Data",
            'width': '120'
        },
        {
            "fieldname": "name_of_journal",
            "label": _("Name of Journal"),
            "fieldtype": "Data",
            'width': '120'
        },
        {
            "fieldname": "name_of_the_conference",
            "label": _("Name of Conference"),
            "fieldtype": "Data",
            'width': '120'
        },
        {
            "fieldname": "financial_year",
            "label": _("Financial Year"),
            "fieldtype": "Link",
            "options": "Fiscal Year",
            'width': '120'
        },
        {
            "fieldname": "place_of_publication",
            "label": _("Place of Publication"),
            "fieldtype": "Data",
            'width': '120'
        },
        {
            "fieldname": "national_international",
            "label": _("Type"),
            "fieldtype": "Select",
            'width': '120'
        },
        {
            "fieldname": "affiliation",
            "label": _("Affiliation"),
            "fieldtype": "Data",
            'width': '120'
        },
        {
            "fieldname": "publisher",
            "label": _("Publisher"),
            "fieldtype": "Data",
            'width': '120'
        },
        {
            "fieldname": "is_ugc_care_listed_",
            "label": _("UGC Care Listed"),
            "fieldtype": "Select",
            'width': '120'
        },
        {
            "fieldname": "proof",
            "label": _("Proof"),
            "fieldtype": "Data",
            'width': '120'
        },
        {
            "fieldname": "page_numbers",
            "label": _("Page Numbers"),
            "fieldtype": "Data",
            'width': '120'
        },
        {
            "fieldname": "citation",
            "label": _("Citation"),
            "fieldtype": "Data",
            'width': '120'
        },
        {
            "fieldname": "issue",
            "label": _("Issue"),
            "fieldtype": "Data",
            'width': '120'
        },
        {
            "fieldname": "volume",
            "label": _("Volume"),
            "fieldtype": "Data",
            'width': '120'
        },
        {
            "fieldname": "status",
            "label": _("Status"),
            "fieldtype": "Data",
            'width': '120'
        },
        {
            "fieldname": "impact_factor",
            "label": _("Impact Factor"),
            "fieldtype": "Data",
            'width': '120'
        },
        {
            "fieldname": "issn_isbn",
            "label": _("IISN/ISBN"),
            "fieldtype": "Data",
            'width': '120'
        },
        {
            "fieldname": "linkdoi",
            "label": _("DOI Link"),
            "fieldtype": "Data",
            'width': '120'
        },
        {
            "fieldname": "indexed",
            "label": _("Indexed"),
            "fieldtype": "Data",
            'width': '120'
        },
        {
            "fieldname": "attachment",
            "label": _("Attachment"),
            "fieldtype": "Data",
            'width': '120'
        }
    ]


def get_cs_data(filters, associated_programs):
    conditions = get_conditions(filters, associated_programs)
    data = frappe.get_all(
        doctype='Publication',
        fields=[
            'publication', 'program', 'instructor', 'academic_year', 'date_of_publication', 'employee_id', 
            'title', 'name_of_journal', 'name_of_the_conference', 'financial_year', 'place_of_publication', 
            'national_international', 'affiliation', 'publisher', 'is_ugc_care_listed_', 'proof', 'page_numbers', 
            'citation', 'volume', 'status', 'impact_factor', 'issn_isbn', 'linkdoi', 'indexed', 'attachment','issue'
        ],
        filters=conditions
    )
    return data

def get_conditions(filters, associated_programs):
    conditions = {}
    for key, value in filters.items():
        if filters.get(key):
            conditions[key] = value

    if associated_programs:
        conditions['program'] = ['in', associated_programs]

    return conditions

def get_chart_data(data):
    if not data:
        return None

    labels = set(entry.program for entry in data)
    sub_labels = set(entry.publication for entry in data)

    data_dict = {label: {sub_label: 0 for sub_label in sub_labels} for label in labels}

    for entry in data:
        if entry.status == "Approved":
            program = entry.program
            publication = entry.publication
            data_dict[program][publication] += 1

    datasets = []

    for sub_label in sub_labels:
        dataset = {
            'name': sub_label,
            'values': [],
        }
        for label in labels:
            dataset['values'].append(data_dict[label][sub_label])
        datasets.append(dataset)

    chart = {
        'data': {
            'labels': list(labels),
            'datasets': datasets
        },
        'type': 'bar',
        'height': 10,
        'width': 10,
    }
    return chart

def get_report_summary(data, associated_programs):
    if not data:
        return None

    all_programs_set = set(associated_programs) if associated_programs else set()

    if not associated_programs:
        all_programs = frappe.get_all(
            doctype='Program',
            fields=['program_name']
        )
        all_programs_set = {entry.program_name for entry in all_programs}

    program_counts = {program: 0 for program in all_programs_set}

    for entry in data:
        if entry.status in {"Approved"}:
            if entry.program in program_counts:
                program_counts[entry.program] += 1

    summary_data = []

    for program, count in program_counts.items():
        summary_data.append({
            'value': count,
            'indicator': 'Green',
            'label': program,
            'datatype': 'Int',
            'width': '20',
        })

    return summary_data

@frappe.whitelist()
def log_current_user_data():
    current_user = frappe.session.user
    result = frappe.db.sql("""
        SELECT 
            e.employee,
            e.custom_program,
            e.user_id,
            e.employee_name,
            p.custom_head_of_department_user_id,
            p.custom_portfolio_coordinator_user_id
        FROM 
            tabEmployee e
        JOIN 
            tabProgram p
        ON 
            e.custom_program = p.program_name
        WHERE 
            e.user_id = %s
    """, (current_user,), as_dict=True)

    return result