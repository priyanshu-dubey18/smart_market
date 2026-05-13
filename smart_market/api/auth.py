# ============================================================
# smart_market/api/auth.py
#
# FRAPPE BACKEND - STEP BY STEP SAMAJHNE KE LIYE:
#
# 1. @frappe.whitelist(allow_guest=True)
#    -> Ye decorator function ko PUBLIC API endpoint banata hai
#    -> allow_guest=True = login ke bina bhi call ho sakta hai
#    -> Bina is decorator ke function call nahi hoga
#
# 2. frappe.cache().set_value(key, value, expires_in_sec=300)
#    -> Redis cache mein data 5 minute ke liye save karo
#    -> OTP store karne ke liye use karte hain
#
# 3. frappe.get_doc({...})
#    -> Frappe database mein naya document banana
#    -> ERPNext ka har "form" ek doctype hai
#
# 4. frappe.db.exists("User", email)
#    -> Check karo database mein record hai ya nahi
#
# 5. frappe.throw(_("message"))
#    -> Error response return karo (frontend pe error aayega)
#
# 6. frappe.sendmail(...)
#    -> Email bhejna (SMTP configured hona chahiye)
# ============================================================

import frappe
import random
import string
from frappe import _
from frappe.utils.password import check_password, update_password


# ─────────────────────────────────────────────
# HELPER FUNCTIONS (Private - no whitelist)
# ─────────────────────────────────────────────

def _generate_otp():
    """6 digit random OTP banao"""
    return ''.join(random.choices(string.digits, k=6))


def _cache_key(contact):
    """Redis cache ki unique key"""
    return f"sm_otp:{contact}"


def _store_otp(contact, otp, extra_data=None):
    """
    OTP ko Redis cache mein save karo - 5 minute ke liye
    contact = phone number ya email (jis pe OTP gaya)
    """
    frappe.cache().set_value(
        _cache_key(contact),
        {
            "otp": otp,
            "attempts": 0,       # galat attempts count
            "verified": False,   # OTP verify hua ya nahi
            "data": extra_data or {}
        },
        expires_in_sec=300  # 5 minute = 300 seconds
    )


def _get_cached_otp(contact):
    """Cache se OTP data lo"""
    return frappe.cache().get_value(_cache_key(contact))


def _clear_cached_otp(contact):
    """OTP use ho gaya toh delete karo"""
    frappe.cache().delete_value(_cache_key(contact))


def _send_otp_email(to_email, otp, name="User"):
    """Email pe OTP bhejo (beautiful HTML template)"""
    frappe.sendmail(
        recipients=[to_email],
        subject="Smart Market - Your OTP Code",
        message=f"""
        <div style="font-family:Arial,sans-serif;max-width:500px;margin:0 auto;
                    padding:30px;background:#f8faff;border-radius:16px;">
            <div style="text-align:center;margin-bottom:24px;">
                <h1 style="color:#6366f1;margin:0;">⚡ Smart<span style="color:#0f172a">Market</span></h1>
            </div>
            <div style="background:white;padding:24px;border-radius:12px;
                        box-shadow:0 2px 8px rgba(0,0,0,0.08);">
                <p style="font-size:16px;color:#374151;">Hello <strong>{name}</strong>,</p>
                <p style="color:#6b7280;">Your verification code is:</p>
                <div style="text-align:center;margin:24px 0;">
                    <div style="display:inline-block;font-size:42px;font-weight:900;
                                letter-spacing:16px;color:#6366f1;padding:20px 32px;
                                background:#eef2ff;border-radius:12px;
                                border:2px dashed #a5b4fc;">
                        {otp}
                    </div>
                </div>
                <p style="color:#ef4444;font-size:14px;text-align:center;">
                    ⏱️ Valid for <strong>5 minutes</strong> only. Do not share with anyone.
                </p>
            </div>
            <p style="text-align:center;color:#9ca3af;font-size:12px;margin-top:16px;">
                Smart Market © 2025. If you didn't request this, ignore this email.
            </p>
        </div>

# <div style="font-family:Arial,sans-serif;max-width:500px;margin:0 auto;
#             padding:30px;background:#f8faff;border-radius:16px;">

#     <!-- Header -->
#     <div style="text-align:center;margin-bottom:24px;">
#         <h1 style="color:#6366f1;margin:0;">
#             ⚡ Smart<span style="color:#0f172a">Market</span>
#         </h1>
#         <p style="color:#6b7280;font-size:13px;">Your trusted marketplace</p>
#     </div>

#     <!-- Main Content -->
#     <div style="background:white;padding:24px;border-radius:12px;
#                 box-shadow:0 2px 8px rgba(0,0,0,0.08);">

#         <p style="font-size:16px;color:#374151;">
#             Hello <strong>{name}</strong> 🎉
#         </p>

#         <p style="color:#6b7280;">
#             Aapki shopping pe humara special <strong>Festive Cashback Offer</strong> 
#             active hai! Aapko mil gaya:
#         </p>

#         <!-- Cashback Amount -->
#         <div style="text-align:center;margin:24px 0;">
#             <div style="display:inline-block;font-size:48px;font-weight:900;
#                         color:#6366f1;padding:20px 40px;
#                         background:#eef2ff;border-radius:12px;
#                         border:2px dashed #a5b4fc;">
#                 🎁 ₹30,000
#             </div>
#             <p style="color:#10b981;font-weight:bold;font-size:18px;margin-top:12px;">
#                 Smart Market Cashback Credit!
#             </p>
#         </div>

#         <p style="color:#6b7280;font-size:14px;text-align:center;">
#             Yeh cashback aapke Smart Market wallet mein add kar diya gaya hai.<br>
#             Apni agli shopping mein use karein!
#         </p>

#         <!-- CTA Button -->
#         <div style="text-align:center;margin-top:24px;">
#             <a href="#" style="background:#6366f1;color:white;padding:12px 32px;
#                                border-radius:8px;text-decoration:none;
#                                font-weight:bold;font-size:16px;">
#                 🛒 Ab Shopping Karein
#             </a>
#         </div>
#     </div>

#     <!-- Footer -->
#     <p style="text-align:center;color:#9ca3af;font-size:12px;margin-top:16px;">
#         Smart Market © 2025 | Terms & Conditions apply.
#     </p>
# </div>

        """,
        now=True  # abhi bhejo, queue mein mat rakho
    )


# ─────────────────────────────────────────────
# STEP 1A: CUSTOMER - OTP bhejo
# Frontend call: smart_market.api.auth.send_otp
# ─────────────────────────────────────────────

@frappe.whitelist(allow_guest=True)
def send_otp(medium, contact, purpose):
    """
    OTP bhejo - phone ya email pe
    medium  = 'phone' ya 'email'
    contact = phone number ya email address
    purpose = 'customer_signup' | 'vendor_signup' | 'reset-email' | 'reset-password'
    """
    if not contact or not medium or not purpose:
        frappe.throw(_("Contact, medium aur purpose sab zaroori hain."))

    # OTP banao
    otp = _generate_otp()

    if medium == "email":
        # Email pe OTP bhejo
        try:
            _send_otp_email(to_email=contact, otp=otp)
        except Exception as e:
            frappe.log_error(str(e), "SM OTP Email Error")
            frappe.throw(_("Email send karne mein error aaya. Admin se contact karo."))

    elif medium == "phone":
        frappe.logger().info(f"[SMART MARKET OTP] Phone: {contact}, OTP: {otp}, Purpose: {purpose}")
        try:
            from frappe.core.doctype.sms_settings.sms_settings import send_sms
            send_sms([contact], f"Your Smart Market OTP is: {otp}. Valid for 5 minutes. Do not share.")
        except Exception as e:
            # SMS fail hone par bhi OTP cache mein save hoga
            try:
                frappe.log_error(str(e), "SM SMS Error")
            except Exception:
                pass
            frappe.logger().warning(f"[SMART MARKET] SMS failed for {contact}. OTP={otp}")
    else:
        frappe.throw(_("Invalid medium. 'phone' ya 'email' hona chahiye."))

    # OTP cache mein save karo
    _store_otp(contact, otp, {"purpose": purpose, "medium": medium})

    # Development mein OTP response mein bhi return karo (production mein remove karna)
    response = {"message": f"OTP sent to {contact}"}
    if frappe.conf.get("developer_mode"):
        response["dev_otp"] = otp
    return response


# ─────────────────────────────────────────────
# STEP 1B: VENDOR - Backend check karo
# Frontend call: smart_market.api.auth.check_vendor_eligibility
# ─────────────────────────────────────────────

@frappe.whitelist(allow_guest=True)
def check_vendor_eligibility(email, full_name):
    """
    Vendor sign up se pehle check karo:
    - Kya is email se koi User hai? YA
    - Kya koi Employee hai is email se?

    Sirf pre-approved log hi vendor ban sakte hain.
    """
    if not email:
        frappe.throw(_("Email zaroori hai."))

    # Check 1: Frappe User table mein dekho
    user_exists = frappe.db.exists("User", {"name": email})

    # Check 2: Employee table mein dekho (company_email ya personal_email)
    employee_exists = frappe.db.exists("Employee", {
        "company_email": email
    }) or frappe.db.exists("Employee", {
        "personal_email": email
    })

    if user_exists or employee_exists:
        return {"eligible": True}
    else:
        frappe.throw(
            _("Aapki email system mein registered nahi hai. Administrator se contact karo.")
        )


# ─────────────────────────────────────────────
# STEP 2: OTP Verify karo
# Frontend call: smart_market.api.auth.verify_otp
# ─────────────────────────────────────────────

@frappe.whitelist(allow_guest=True)
def verify_otp(contact, otp, purpose):
    """
    User ne OTP enter kiya - check karo sahi hai ya nahi
    3 se zyada galat attempts pe OTP delete ho jaata hai
    """
    if not contact or not otp:
        frappe.throw(_("Contact aur OTP zaroori hain."))

    cached = _get_cached_otp(contact)

    # OTP mila nahi? Expire ho gaya hoga
    if not cached:
        frappe.throw(_("OTP expire ho gaya. Dobara request karo."))

    # Zyada galat attempts?
    if cached.get("attempts", 0) >= 3:
        _clear_cached_otp(contact)
        frappe.throw(_("3 baar galat OTP. Naya OTP request karo."))

    # OTP match karo
    if str(cached["otp"]) != str(otp):
        cached["attempts"] = cached.get("attempts", 0) + 1
        # Updated attempts cache mein save karo
        frappe.cache().set_value(_cache_key(contact), cached, expires_in_sec=300)
        remaining = 3 - cached["attempts"]
        frappe.throw(_(f"Galat OTP. {remaining} attempts baaki hain."))

    # OTP sahi hai! verified mark karo
    cached["verified"] = True
    frappe.cache().set_value(_cache_key(contact), cached, expires_in_sec=300)

    return {"message": "OTP verified successfully!"}


# ─────────────────────────────────────────────
# STEP 3A: CUSTOMER - Account banao
# Frontend call: smart_market.api.auth.customer_signup
# ─────────────────────────────────────────────

@frappe.whitelist(allow_guest=True)
def customer_signup(full_name, email, phone, username, password, user_type):
    """
    Customer ka account Frappe mein banao.

    Kya hota hai andar:
    - frappe.get_doc() se ek nayi User document banate hain
    - .insert() se database mein save hoti hai
    - frappe.db.commit() se permanently save hota hai
    """
    if not all([full_name, email, phone, username, password]):
        frappe.throw(_("Sab fields zaroori hain."))

    # Pehle check karo OTP verify hua tha
    cached = _get_cached_otp(email)  # email pe OTP gaya tha
    if not cached or not cached.get("verified"):
        frappe.throw(_("OTP verify nahi hua. Dobara try karo."))

    # Email already registered?
    if frappe.db.exists("User", email):
        frappe.throw(_("Yeh email pehle se registered hai. Sign In karo."))

    # Username already liya gaya?
    if frappe.db.exists("User", {"username": username}):
        frappe.throw(_("Yeh username pehle se liya ja chuka hai. Koi aur username chunein."))

    # Name ko first_name aur last_name mein todna
    name_parts = full_name.strip().split(" ", 1)
    first_name = name_parts[0]
    last_name = name_parts[1] if len(name_parts) > 1 else ""

    try:
        # ─────────────────────────────────────────
        # Frappe mein User document banana
        # ─────────────────────────────────────────
        user_doc = frappe.get_doc({
            "doctype": "User",        # Frappe ki User table
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "username": username,
            "mobile_no": phone,
            "new_password": password,  # Frappe khud hash kar leta hai
            "user_type": "Website User",  # Website User = customer (desk access nahi)
            "send_welcome_email": 0,   # Welcome email mat bhejo
            "roles": [
                {"role": "Customer"}   # Customer role assign karo
            ]
        })

        user_doc.insert(ignore_permissions=True)  # Admin permission ke bina bhi insert ho
        frappe.db.commit()  # Database mein permanently save karo

        # OTP cache clear karo
        _clear_cached_otp(email)

        # Auto login karo user ko
        frappe.local.login_manager.login_as(email)

        return {
            "message": {
                "success": True,
                "full_name": full_name,
                "email": email,
                "username": username,
                "user_type": "customer"
            }
        }

    except frappe.DuplicateEntryError:
        frappe.throw(_("Yeh email ya username pehle se exist karta hai."))
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Customer Signup Error")
        frappe.throw(_(str(e)))


# ─────────────────────────────────────────────
# STEP 3B: VENDOR - Account banao
# Frontend call: smart_market.api.auth.vendor_signup
# ─────────────────────────────────────────────

@frappe.whitelist(allow_guest=True)
def vendor_signup(full_name, email, phone, username, password, user_type):
    """
    Vendor ka account banao.
    Vendor ke liye user pehle se exist karta hai system mein,
    toh hum sirf username set karte hain.
    """
    if not all([full_name, email, phone, username, password]):
        frappe.throw(_("Sab fields zaroori hain."))

    # OTP verified tha?
    cached = _get_cached_otp(email)
    if not cached or not cached.get("verified"):
        frappe.throw(_("OTP verify nahi hua. Dobara try karo."))

    try:
        # Vendor ka User already exist karta hai
        if frappe.db.exists("User", email):
            user_doc = frappe.get_doc("User", email)
            user_doc.username = username
            user_doc.mobile_no = phone
            user_doc.save(ignore_permissions=True)
            # Password update karo
            update_password(email, password)
        else:
            # Naya user banao (Employee tha, User nahi tha)
            name_parts = full_name.strip().split(" ", 1)
            user_doc = frappe.get_doc({
                "doctype": "User",
                "email": email,
                "first_name": name_parts[0],
                "last_name": name_parts[1] if len(name_parts) > 1 else "",
                "username": username,
                "mobile_no": phone,
                "new_password": password,
                "user_type": "System User",  # Vendor = System User (desk access)
                "send_welcome_email": 0,
                "roles": [
                    {"role": "Vendor"}  # Vendor role (pehle banani hogi Frappe mein)
                ]
            })
            user_doc.insert(ignore_permissions=True)

        frappe.db.commit()
        _clear_cached_otp(email)
        frappe.local.login_manager.login_as(email)

        return {
            "message": {
                "success": True,
                "full_name": full_name,
                "email": email,
                "username": username,
                "user_type": "vendor"
            }
        }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Vendor Signup Error")
        frappe.throw(_(str(e)))


# ─────────────────────────────────────────────
# STEP 4: LOGIN
# Frontend call: smart_market.api.auth.login
# ─────────────────────────────────────────────

@frappe.whitelist(allow_guest=True)
def login(identifier, password):
    """
    User ko login karo.
    identifier = email ya username dono accept karta hai

    Frappe ka login system:
    - frappe.local.login_manager.authenticate() = password check
    - frappe.local.login_manager.post_login() = session banana
    """
    if not identifier or not password:
        frappe.throw(_("Email/Username aur password zaroori hain."))

    # Pehle email dhundho agar username diya hai
    email = identifier
    if "@" not in identifier:
        # Username se email dhundho
        user = frappe.db.get_value("User", {"username": identifier}, "name")
        if not user:
            frappe.throw(_("Username exist nahi karta."))
        email = user

    # User exist karta hai?
    if not frappe.db.exists("User", email):
        frappe.throw(_("Koi account nahi mila is email/username se."))

    # Password check karo
    try:
        check_password(email, password)
    except frappe.AuthenticationError:
        frappe.throw(_("Galat password. Dobara try karo."))

    # Login session banao
    frappe.local.login_manager.login_as(email)

    # User ki info return karo
    user_doc = frappe.get_doc("User", email)

    return {
        "message": {
            "success": True,
            "email": email,
            "full_name": user_doc.full_name,
            "user_type": user_doc.user_type,
            "username": user_doc.username or ""
        }
    }


# ─────────────────────────────────────────────
# STEP 5A: RESET EMAIL / USERNAME
# Frontend call: smart_market.api.auth.reset_email
# ─────────────────────────────────────────────

@frappe.whitelist(allow_guest=True)
def reset_email(phone, new_email, new_username):
    """
    OTP verify ke baad email ya username update karo.
    Phone se user dhundhte hain.
    """
    if not phone:
        frappe.throw(_("Phone number zaroori hai."))
    if not new_email and not new_username:
        frappe.throw(_("Naya email ya username toh dena hoga."))

    # OTP verified tha?
    cached = _get_cached_otp(phone)
    if not cached or not cached.get("verified"):
        frappe.throw(_("OTP verify nahi hua. Dobara try karo."))

    # Phone se user dhundho
    user_name = frappe.db.get_value("User", {"mobile_no": phone}, "name")
    if not user_name:
        frappe.throw(_("Is phone number se koi account nahi mila."))

    user_doc = frappe.get_doc("User", user_name)

    if new_email and new_email != user_doc.email:
        if frappe.db.exists("User", new_email):
            frappe.throw(_("Yeh email pehle se kisi aur account mein hai."))
        user_doc.email = new_email

    if new_username and new_username != user_doc.username:
        if frappe.db.exists("User", {"username": new_username}):
            frappe.throw(_("Yeh username pehle se liya gaya hai."))
        user_doc.username = new_username

    user_doc.save(ignore_permissions=True)
    frappe.db.commit()
    _clear_cached_otp(phone)

    return {"message": "Email/Username successfully update ho gaya!"}


# ─────────────────────────────────────────────
# STEP 5B: RESET PASSWORD
# Frontend call: smart_market.api.auth.reset_password
# ─────────────────────────────────────────────

@frappe.whitelist(allow_guest=True)
def reset_password(email, new_password):
    """
    OTP verify ke baad password update karo.
    OTP email pe gaya tha toh email se user dhundhte hain.
    """
    if not email or not new_password:
        frappe.throw(_("Email aur naya password zaroori hain."))

    if len(new_password) < 8:
        frappe.throw(_("Password kam se kam 8 characters ka hona chahiye."))

    # OTP verified tha?
    cached = _get_cached_otp(email)
    if not cached or not cached.get("verified"):
        frappe.throw(_("OTP verify nahi hua. Dobara try karo."))

    # User exist karta hai?
    if not frappe.db.exists("User", email):
        frappe.throw(_("Is email se koi account nahi mila."))

    # Password update karo
    # Frappe ka update_password function password hash karke save karta hai
    update_password(email, new_password)
    frappe.db.commit()
    _clear_cached_otp(email)

    return {"message": "Password successfully reset ho gaya! Ab sign in karo."}
