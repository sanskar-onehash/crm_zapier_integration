import frappe


def after_uninstall():
    remove_zapier_manager_role()


def remove_zapier_manager_role():
    if frappe.db.exists("Role", "Zapier Manager"):
        frappe.get_doc("Role", "Zapier Manager").delete()
        frappe.db.commit()
