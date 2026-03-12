# # Copyright (c) 2026, Hybrowlabs and contributors
# # For license information, please see license.txt

# import frappe

# def execute(filters=None):
#     filters = filters or {}
#     columns = get_columns()
#     data = get_data(filters)
#     return columns, data


# def get_columns():
#     return [
#         {"label": "Branch", "fieldname": "branch", "fieldtype": "Data", "width": 120},
#         {"label": "Quotation", "fieldname": "quotation", "fieldtype": "Link", "options": "Quotation", "width": 200},
#         {"label": "Date", "fieldname": "date", "fieldtype": "Date", "width": 120},
#         {"label": "SO Number", "fieldname": "so_number", "fieldtype": "Link", "options": "Sales Order", "width": 150},
#         {"label": "Quotation Title", "fieldname": "quotation_title", "fieldtype": "Data", "width": 200},
#         {"label": "Item Code", "fieldname": "item_code", "fieldtype": "Link", "options": "Item", "width": 150},
#         {"label": "Item Name", "fieldname": "item_name", "fieldtype": "Data", "width": 200},
#         {"label": "Brand", "fieldname": "brand", "fieldtype": "Data", "width": 120},
#         {"label": "QI Qty", "fieldname": "qi_qty", "fieldtype": "Data", "width": 120},
#         {"label": "Sum SO Qty", "fieldname": "so_qty", "fieldtype": "Data", "width": 120},
#         {"label": "Diff Qty", "fieldname": "diff_qty", "fieldtype": "Data", "width": 120},
#         {"label": "QI Rate", "fieldname": "qi_rate", "fieldtype": "Currency", "width": 120},
#         {"label": "QI Total", "fieldname": "qi_total", "fieldtype": "Currency", "width": 120},
#         {"label": "SI Rate", "fieldname": "si_rate", "fieldtype": "Currency", "width": 120},
#         {"label": "SO Total", "fieldname": "so_total", "fieldtype": "Currency", "width": 120},
#         {"label": "Reason", "fieldname": "reason", "fieldtype": "Data", "width": 200},
#     ]


# def get_data(filters):
#     conditions = ""
#     values = {}

#     if filters.get("branch"):
#         conditions += " AND q.custom_branch = %(branch)s"
#         values["branch"] = filters.get("branch")

#     return frappe.db.sql(f"""
#         SELECT
#             q.custom_branch AS branch,
#             q.name AS quotation,
#             q.transaction_date AS date,
#             soi.parent AS so_number,
#             q.title AS quotation_title,
#             qi.item_code,
#             qi.item_name,
#             i.brand,
#             CONCAT(CAST(qi.qty AS UNSIGNED), ' ', qi.uom) AS qi_qty,
#             CONCAT(CAST(SUM(soi.qty) AS UNSIGNED), ' ', soi.uom) AS so_qty,
#             CONCAT('<span style="color:',
#                 CASE 
#                     WHEN (COALESCE(SUM(soi.qty),0) - qi.qty) < 0 
#                     THEN 'red' ELSE 'green'
#                 END,
#                 '">',
#                 CAST(COALESCE(SUM(soi.qty),0) - qi.qty AS SIGNED),
#                 ' ', qi.uom,
#                 '</span>'
#             ) AS diff_qty,
#             qi.rate AS qi_rate,
#             q.total AS qi_total,
#             soi.rate AS si_rate,
#             so.total AS so_total,
#             q.custom_remark AS reason
#         FROM
#             `tabQuotation` q
#         LEFT JOIN
#             `tabQuotation Item` qi ON q.name = qi.parent
#         LEFT JOIN
#             `tabItem` i ON qi.item_code = i.name
#         LEFT JOIN
#             `tabSales Order Item` soi 
#                 ON q.name = soi.prevdoc_docname
#                 AND qi.item_code = soi.item_code
#         LEFT JOIN
#             `tabSales Order` so ON soi.parent = so.name
#         WHERE
#             q.docstatus = 1
#             {conditions}
#         GROUP BY
#             q.custom_branch,
#             q.name,
#             q.transaction_date,
#             soi.parent,
#             q.title,
#             qi.item_code,
#             qi.item_name,
#             i.brand,
#             qi.qty,
#             qi.uom
#         ORDER BY
#             q.name ASC
#     """, values, as_dict=True)


# Copyright (c) 2026, Hybrowlabs and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    filters = filters or {}

    # If the checkbox 'show_summary' is checked, show summary report
    if filters.get("show_summary"):
        columns = get_summary_columns()
        data = get_summary_data(filters)
    else:
        columns = get_columns()
        data = get_data(filters)

    return columns, data


# -------------------------
# Columns for Detailed Report
# -------------------------
def get_columns():
    return [
        {"label": "Branch", "fieldname": "branch", "fieldtype": "Data", "width": 120},
        {"label": "Quotation", "fieldname": "quotation", "fieldtype": "Link", "options": "Quotation", "width": 200},
        {"label": "Date", "fieldname": "date", "fieldtype": "Date", "width": 120},
        {"label": "SO Number", "fieldname": "so_number", "fieldtype": "Link", "options": "Sales Order", "width": 150},
        {"label": "Quotation Title", "fieldname": "quotation_title", "fieldtype": "Data", "width": 200},
        {"label": "Item Code", "fieldname": "item_code", "fieldtype": "Link", "options": "Item", "width": 150},
        {"label": "Item Name", "fieldname": "item_name", "fieldtype": "Data", "width": 200},
        {"label": "Brand", "fieldname": "brand", "fieldtype": "Data", "width": 120},
        {"label": "QI Qty", "fieldname": "qi_qty", "fieldtype": "Data", "width": 120},
        {"label": "Sum SO Qty", "fieldname": "so_qty", "fieldtype": "Data", "width": 120},
        {"label": "Diff Qty", "fieldname": "diff_qty", "fieldtype": "Data", "width": 120},
        {"label": "QI Rate", "fieldname": "qi_rate", "fieldtype": "Currency", "width": 120},
        {"label": "QI Total", "fieldname": "qi_total", "fieldtype": "Currency", "width": 120},
        {"label": "SI Rate", "fieldname": "si_rate", "fieldtype": "Currency", "width": 120},
        {"label": "SO Total", "fieldname": "so_total", "fieldtype": "Currency", "width": 120},
        {"label": "Reason", "fieldname": "reason", "fieldtype": "Data", "width": 200},
    ]




# -------------------------
# Detailed Report Data
# -------------------------
def get_data(filters):
    conditions = ""
    values = {}

    if filters.get("branch"):
        conditions += " AND q.custom_branch = %(branch)s"
        values["branch"] = filters.get("branch")

    return frappe.db.sql(f"""
        SELECT
            q.custom_branch AS branch,
            q.name AS quotation,
            q.transaction_date AS date,
            soi.parent AS so_number,
            q.title AS quotation_title,
            qi.item_code,
            qi.item_name,
            i.brand,
            CONCAT(CAST(qi.qty AS UNSIGNED), ' ', qi.uom) AS qi_qty,
            CONCAT(CAST(SUM(soi.qty) AS UNSIGNED), ' ', soi.uom) AS so_qty,
            CONCAT('<span style="color:',
                CASE 
                    WHEN (COALESCE(SUM(soi.qty),0) - qi.qty) < 0 
                    THEN 'red' ELSE 'green'
                END,
                '">',
                CAST(COALESCE(SUM(soi.qty),0) - qi.qty AS SIGNED),
                ' ', qi.uom,
                '</span>'
            ) AS diff_qty,
            qi.rate AS qi_rate,
            q.total AS qi_total,
            soi.rate AS si_rate,
            so.total AS so_total,
            q.custom_remark AS reason
        FROM
            `tabQuotation` q
        LEFT JOIN
            `tabQuotation Item` qi ON q.name = qi.parent
        LEFT JOIN
            `tabItem` i ON qi.item_code = i.name
        LEFT JOIN
            `tabSales Order Item` soi 
                ON q.name = soi.prevdoc_docname
                AND soi.prevdoc_doctype = 'Quotation'
        LEFT JOIN
            `tabSales Order` so ON soi.parent = so.name
        WHERE
            q.docstatus = 1
            {conditions}
        GROUP BY
            q.custom_branch,
            q.name,
            q.transaction_date,
            soi.parent,
            q.title,
            qi.item_code,
            qi.item_name,
            i.brand,
            qi.qty,
            qi.uom
        ORDER BY
            q.name ASC
    """, values, as_dict=True)


def get_summary_columns():
    return [
        {"label": "Quotation", "fieldname": "quotation", "fieldtype": "Link", "options": "Quotation", "width": 200},
        {"label": "Quotation Total", "fieldname": "quotation_total", "fieldtype": "Currency", "width": 150},
        {"label": "Sales Orders", "fieldname": "sales_order", "fieldtype": "Data", "width": 250},
        {"label": "Total Sales Orders", "fieldname": "total_so", "fieldtype": "Currency", "width": 150},
    ]


def get_summary_data(filters):
    conditions = ""
    values = {}

    if filters.get("branch"):
        conditions += " AND q.custom_branch = %(branch)s"
        values["branch"] = filters.get("branch")

    return frappe.db.sql(f"""
        SELECT
            q.name AS quotation,
            q.total AS quotation_total,
            GROUP_CONCAT(DISTINCT so.name ORDER BY so.name SEPARATOR ', ') AS sales_order,
            COALESCE(SUM(DISTINCT so.total), 0) AS total_so
        FROM
            `tabQuotation` q
        LEFT JOIN `tabSales Order Item` soi
            ON soi.prevdoc_docname = q.name
            AND soi.docstatus = 1
        LEFT JOIN `tabSales Order` so
            ON so.name = soi.parent
            AND so.docstatus = 1
        WHERE
            q.docstatus = 1
            {conditions}
        GROUP BY
            q.name, q.total
        ORDER BY
            q.name ASC
    """, values, as_dict=True)