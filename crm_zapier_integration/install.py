import frappe


def after_install():
    add_zapier_manager_role()


def add_zapier_manager_role():
    if not frappe.db.exists("Role", "Zapier Manager"):
        frappe.get_doc({"doctype": "Role", "role_name": "Zapier Manager"}).insert()
        frappe.db.commit()
