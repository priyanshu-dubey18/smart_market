no_cache = 1

def get_context(context):
	import frappe
	# Redirect already logged-in users to home
	if frappe.session.user != "Guest":
		frappe.local.response["type"] = "redirect"
		frappe.local.response["location"] = "/"
		return

	context.no_header = 1
	context.no_footer = 1
	context.no_sidebar = 1
	context.title = "Smart Market - Welcome"
