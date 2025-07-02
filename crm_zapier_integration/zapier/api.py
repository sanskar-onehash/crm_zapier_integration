import frappe

from crm_zapier_integration.zapier.utils import docfields_to_zap_fields


@frappe.whitelist()
def get_zapier_fields(doctype):
    meta = frappe.get_meta(doctype, True)
    zap_fields = docfields_to_zap_fields(meta.fields)
    return zap_fields
