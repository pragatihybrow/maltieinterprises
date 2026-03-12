// Copyright (c) 2026, Hybrowlabs and contributors
// For license information, please see license.txt

// frappe.query_reports["Quotation  Vs Sales Order Report"] = {
//     "filters": [
//         {
//             "fieldname": "branch",
//             "label": __("Branch"),
//             "fieldtype": "Link",
//             "options": "Branch",
//             "default": "",
//             "reqd": 0
//         }
//     ]
// };

frappe.query_reports["Quotation  Vs Sales Order Report"] = {
    "filters": [
        {
            "fieldname": "branch",
            "label": __("Branch"),
            "fieldtype": "Link",
            "options": "Branch",
            "default": "",
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