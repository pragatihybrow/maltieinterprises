// // Copyright (c) 2026, Hybrowlabs and contributors
// // For license information, please see license.txt


// frappe.query_reports["Quotation  Vs Sales Order Report"] = {
//     "filters": [
//         {
//             "fieldname": "branch",
//             "label": __("Branch"),
//             "fieldtype": "Link",
//             "options": "Branch",
//             "default": "",
//             "reqd": 0
//         },
//         {
//             "fieldname": "from_date",
//             "label": __("From Date"),
//             "fieldtype": "Date",
//             "default": frappe.datetime.get_today(),
//             "reqd": 0
//         },
//         {
//             "fieldname": "to_date",
//             "label": __("To Date"),
//             "fieldtype": "Date",
//             "default": frappe.datetime.get_today(),
//             "reqd": 0
//         },
//         {
//             "fieldname": "show_summary",
//             "label": __("Show Summary"),
//             "fieldtype": "Check",
//             "default": 0
//         }
//     ]
// };


// Copyright (c) 2026, Hybrowlabs and contributors
// For license information, please see license.txt

frappe.query_reports["Quotation  Vs Sales Order Report"] = {
    "filters": [
        {
            "fieldname": "branch",
            "label": __("Branch"),
            "fieldtype": "MultiSelectList",
            "get_data": function(txt) {
                return frappe.db.get_link_options("Branch", txt);
            },
            "default": "",
            "reqd": 0
        },
        {
            "fieldname": "from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.get_today(),
            "reqd": 0
        },
        {
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.get_today(),
            "reqd": 0
        },
        {
            "fieldname": "show_summary",
            "label": __("Show Summary"),
            "fieldtype": "Check",
            "default": 0
        }
    ]
};