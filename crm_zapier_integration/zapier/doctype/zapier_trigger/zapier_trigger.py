# Copyright (c) 2025, OneHash and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class ZapierTrigger(Document):

    def unsubscribe_trigger(self):
        self.update({"disabled": True}).save(ignore_permissions=True)
