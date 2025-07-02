import frappe


def docfields_to_zap_fields(docfields):
    zap_fields = []
    for docfield in docfields:
        if docfield.fieldtype in [
            "Heading",
            "Button",
            "Section Break",
            "Tab Break",
            "Column Break",
        ]:
            continue

        zap_field = {
            "key": docfield.fieldname,
            "label": docfield.label,
            "type": fieldtype_to_zaptype(docfield.fieldtype),
            "required": docfield.reqd,
            "default": docfield.default,
        }
        if docfield.fieldtype in ["Select", "Autocomplete"]:
            zap_field["choices"] = docfield.options.split("\n")
        elif docfield.fieldtype in ["Table", "Table MultiSelect"]:
            # TODO:
            # List = True, not working
            zap_field["children"] = docfields_to_zap_fields(
                frappe.get_meta(docfield.options, True).fields
            )
            zap_field["list"] = True
        elif docfield.fieldtype in ["Link", "Dynamic Link"]:
            # INFO:
            # Currently there's no feature or workaround available for such dynamic list
            # Dynamic dropdown can only refer to existing resource
            pass
        zap_fields.append(zap_field)
    return zap_fields


def fieldtype_to_zaptype(fieldtype):
    zaptype = "text"

    if fieldtype in ["Attach", "Attach Image", "Image", "Signature"]:
        zaptype = "file"

    elif fieldtype in [
        "Barcode",
        "Code",
        "Color",
        "Geolocation",
        "HTML",
        "HTML Editor",
        "JSON",
        "Markdown Editor",
        "Text Editor",
    ]:
        zaptype = "code"

    elif fieldtype == "Check":
        zaptype = "boolean"

    elif fieldtype == "Int":
        zaptype = "integer"

    elif fieldtype in ["Currency", "Float", "Rating", "Percent", "Duration"]:
        zaptype = "number"

    elif fieldtype in [
        "Data",
        "Dynamic Link",
        "Email",
        "Select",
        "Link",
        "Phone",
        "Icon",
        "Autocomplete",
    ]:
        zaptype = "string"

    elif fieldtype in ["Date", "Datetime", "Time"]:
        zaptype = "datetime"

    elif fieldtype == "Password":
        zaptype = "password"

    return zaptype
