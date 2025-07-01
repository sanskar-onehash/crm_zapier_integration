import frappe
import json
import requests


def handle_doc_event(doc, method):
    if not frappe.flags.in_migrate and doc.doctype != "Error Log":
        if method == "on_update" and doc.modified == doc.creation:
            return
        zap_triggers = frappe.db.get_all(
            "Zapier Trigger",
            ["name", "target_url"],
            {
                "trigger_doctype": doc.doctype,
                "trigger_method": method,
                "disabled": False,
            },
        )
        data = json.dumps([doc.as_dict(convert_dates_to_str=True)])
        for zap_trigger in zap_triggers:
            try:
                res = requests.post(zap_trigger.target_url, json=data)
                if res.status_code == 410:
                    # No longer active
                    frappe.get_doc(
                        "Zapier Trigger", zap_trigger.name
                    ).unsubscribe_trigger()

            except Exception as e:
                frappe.log_error(
                    "Error triggering Zapier trigger", {"data": data, "error": str(e)}
                )


@frappe.whitelist()
def subscribe_doctypes(target_url):
    frappe.log_error("subscribe_doctypes", target_url)
    add_webhook("DocType", "after_insert", target_url)


@frappe.whitelist()
def unsubscribe_doctypes(subsciption_data):
    frappe.log_error("unsubscribe_doctypes", subsciption_data)
    remove_webhook(subsciption_data)


@frappe.whitelist()
def get_doctypes():
    page = int(frappe.form_dict.get("page", 0))
    limit = int(frappe.form_dict.get("limit", 0))
    doctypes = frappe.db.get_list(
        "DocType",
        ["name", "creation"],
        {"istable": 0},
        order_by="name asc",
        limit_start=page * limit,
        limit_page_length=limit,
    )
    return [
        {
            "id": doctype.name,
            "name": doctype.name,
            "created_at": doctype.creation,
        }
        for doctype in doctypes
    ]


@frappe.whitelist()
def add_webhook(trigger_doctype, trigger_method, target_url):
    frappe.log_error(
        "add_webhook",
        {
            "trigger_doctype": trigger_doctype,
            "trigger_method": trigger_method,
            "target_url": target_url,
        },
    )
    if not frappe.db.exists("DocType", trigger_doctype):
        frappe.throw("DocType not found")

    doc = frappe.get_doc(
        {
            "doctype": "Zapier Trigger",
            "trigger_doctype": trigger_doctype,
            "trigger_method": trigger_method,
            "target_url": target_url,
        },
    ).insert(ignore_permissions=True)
    return {"id": doc.name}


@frappe.whitelist()
def remove_webhook(subsciption_data):
    frappe.log_error("remove_webhook", subsciption_data)
    if not frappe.db.exists("Zapier Trigger", subsciption_data.get("id")):
        frappe.throw("No Webhook to Delete")

    frappe.get_doc("Zapier Trigger", subsciption_data.get("id")).unsubscribe_trigger()
