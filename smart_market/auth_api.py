# Copyright (c) 2026, Smart Market contributors
# Authentication API for Customer and Vendor registration

import frappe
import random
import string
from frappe import _
from frappe.utils.password import check_password, update_password


def _generate_otp():
	return ''.join(random.choices(string.digits, k=6))


def _store_otp(email, otp, data=None):
	frappe.cache().set_value(f"sm_otp:{email}", {
		"otp": otp,
		"data": data or {},
		"attempts": 0,
		"verified": False
	}, expires_in_sec=300)


def _get_otp(email):
	return frappe.cache().get_value(f"sm_otp:{email}")


def _clear_otp(email):
	frappe.cache().delete_value(f"sm_otp:{email}")


@frappe.whitelist(allow_guest=True)
def send_customer_otp(full_name, email, phone, password):
	"""Step 1: Validate customer info and send OTP to email"""
	if not full_name or not email or not phone or not password:
		return {"success": False, "message": _("All fields are required")}

	if frappe.db.exists("User", email):
		return {"success": False, "message": _("Email already registered. Please sign in.")}

	if len(password) < 6:
		return {"success": False, "message": _("Password must be at least 6 characters")}

	otp = _generate_otp()
	_store_otp(email, otp, {
		"full_name": full_name,
		"email": email,
		"phone": phone,
		"password": password,
		"type": "customer"
	})

	try:
		frappe.sendmail(
			recipients=[email],
			subject="Smart Market - Email Verification OTP",
			message=f"""
			<div style="font-family:sans-serif;max-width:500px;margin:0 auto;padding:24px;">
				<h2 style="color:#6c63ff">Smart Market</h2>
				<p>Hello <strong>{full_name}</strong>,</p>
				<p>Your OTP for registration is:</p>
				<div style="font-size:36px;font-weight:700;letter-spacing:12px;color:#6c63ff;
				            padding:20px;background:#f5f5ff;border-radius:12px;
				            text-align:center;margin:16px 0">{otp}</div>
				<p style="color:#888">This OTP is valid for <strong>5 minutes</strong>. Do not share it with anyone.</p>
			</div>
			""",
			now=True
		)
	except Exception as e:
		frappe.log_error(str(e), "SM OTP Email Error")

	return {"success": True, "message": _("OTP sent to {0}").format(email)}


@frappe.whitelist(allow_guest=True)
def send_vendor_otp(email, password):
	"""Step 1 for vendor: Verify existing backend credentials then send OTP"""
	if not email or not password:
		return {"success": False, "message": _("Email and password are required")}

	# Check if user exists in Frappe
	if not frappe.db.exists("User", email):
		return {"success": False, "message": _("No backend account found with this email. Contact your administrator.")}

	# Verify password against Frappe's user database
	try:
		check_password(email, password)
	except frappe.AuthenticationError:
		return {"success": False, "message": _("Invalid credentials. Please use your system password.")}
	except Exception:
		return {"success": False, "message": _("Authentication failed. Please try again.")}

	otp = _generate_otp()
	_store_otp(email, otp, {"email": email, "type": "vendor"})

	try:
		frappe.sendmail(
			recipients=[email],
			subject="Smart Market - Vendor Portal OTP",
			message=f"""
			<div style="font-family:sans-serif;max-width:500px;margin:0 auto;padding:24px;">
				<h2 style="color:#6c63ff">Smart Market - Vendor Portal</h2>
				<p>Your OTP for vendor portal access is:</p>
				<div style="font-size:36px;font-weight:700;letter-spacing:12px;color:#6c63ff;
				            padding:20px;background:#f5f5ff;border-radius:12px;
				            text-align:center;margin:16px 0">{otp}</div>
				<p style="color:#888">Valid for <strong>5 minutes</strong>. Do not share.</p>
			</div>
			""",
			now=True
		)
	except Exception as e:
		frappe.log_error(str(e), "SM Vendor OTP Email Error")

	return {"success": True, "message": _("OTP sent to {0}").format(email)}


@frappe.whitelist(allow_guest=True)
def verify_otp(email, otp):
	"""Step 2: Verify the OTP entered by user"""
	cached = _get_otp(email)
	if not cached:
		return {"success": False, "message": _("OTP expired. Please request a new one.")}

	if cached.get("attempts", 0) >= 3:
		_clear_otp(email)
		return {"success": False, "message": _("Too many failed attempts. Please request a new OTP.")}

	if cached["otp"] != str(otp):
		cached["attempts"] = cached.get("attempts", 0) + 1
		frappe.cache().set_value(f"sm_otp:{email}", cached, expires_in_sec=300)
		remaining = 3 - cached["attempts"]
		return {"success": False, "message": _("Invalid OTP. {0} attempts remaining.").format(remaining)}

	cached["verified"] = True
	frappe.cache().set_value(f"sm_otp:{email}", cached, expires_in_sec=300)
	return {"success": True, "message": _("OTP verified successfully!")}


@frappe.whitelist(allow_guest=True)
def set_password_and_register(email, new_password, confirm_password):
	"""Step 3: Set new password and complete registration"""
	if new_password != confirm_password:
		return {"success": False, "message": _("Passwords do not match")}

	if len(new_password) < 6:
		return {"success": False, "message": _("Password must be at least 6 characters")}

	cached = _get_otp(email)
	if not cached or not cached.get("verified"):
		return {"success": False, "message": _("OTP verification required. Please start again.")}

	user_type = cached.get("data", {}).get("type")

	try:
		if user_type == "customer":
			data = cached["data"]
			full_name = data.get("full_name", "")
			names = full_name.split(" ", 1)

			user = frappe.get_doc({
				"doctype": "User",
				"email": email,
				"first_name": names[0],
				"last_name": names[1] if len(names) > 1 else "",
				"mobile_no": data.get("phone", ""),
				"new_password": new_password,
				"user_type": "Website User",
				"send_welcome_email": 0,
				"roles": [{"role": "Customer"}]
			})
			user.insert(ignore_permissions=True)
			frappe.db.commit()

		elif user_type == "vendor":
			update_password(email, new_password)
			frappe.db.commit()
		else:
			return {"success": False, "message": _("Invalid session. Please start again.")}

		_clear_otp(email)

		# Auto login after registration
		frappe.local.login_manager.login_as(email)

		return {
			"success": True,
			"message": _("Registration successful! Welcome to Smart Market."),
			"redirect": "/"
		}

	except frappe.DuplicateEntryError:
		return {"success": False, "message": _("User already exists. Please sign in.")}
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "SM Registration Error")
		return {"success": False, "message": str(e)}
