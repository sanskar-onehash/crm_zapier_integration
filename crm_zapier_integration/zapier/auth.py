import frappe


@frappe.whitelist()
def verify_auth():
    return frappe.session.user
