import frappe


COMPANY = "Whole Sale"

# ─── Master lists ─────────────────────────────────────────────────────────────

ITEM_GROUPS = [
    "Grocery & Staples",
    "Beverages",
    "Personal Care",
    "Household",
    "Spices & Condiments",
]

SUPPLIER_GROUPS = ["Distributor", "Manufacturer"]

CUSTOMER_GROUPS = ["Retailer", "Wholesaler"]

SUPPLIERS = [
    {
        "supplier_name": "Anil Traders",
        "supplier_group": "Distributor",
        "country": "India",
        "items": ["SUGAR-001", "RICE-001", "FLOUR-001", "SALT-001"],
    },
    {
        "supplier_name": "Rajesh Wholesale Pvt Ltd",
        "supplier_group": "Distributor",
        "country": "India",
        "items": ["OIL-001", "GHEE-001", "PULSES-001", "CHANA-001"],
    },
    {
        "supplier_name": "Sharma & Sons Distributors",
        "supplier_group": "Distributor",
        "country": "India",
        "items": ["TEA-001", "COFFEE-001", "BISCUIT-001"],
    },
    {
        "supplier_name": "Verma FMCG Suppliers",
        "supplier_group": "Distributor",
        "country": "India",
        "items": ["SOAP-001", "DETERGENT-001", "SHAMPOO-001", "TOOTHPASTE-001"],
    },
]

CUSTOMERS = [
    {
        "customer_name": "City Kirana Store",
        "customer_group": "Retailer",
        "territory": "India",
    },
    {
        "customer_name": "Metro General Store",
        "customer_group": "Retailer",
        "territory": "India",
    },
    {
        "customer_name": "Sonu & Brothers Traders",
        "customer_group": "Wholesaler",
        "territory": "India",
    },
    {
        "customer_name": "Laxmi Provision Store",
        "customer_group": "Retailer",
        "territory": "India",
    },
    {
        "customer_name": "Gupta Departmental",
        "customer_group": "Retailer",
        "territory": "India",
    },
    {
        "customer_name": "Ravi Wholesale Hub",
        "customer_group": "Wholesaler",
        "territory": "India",
    },
]

# item_code, item_name, item_group, stock_uom, buying_price, selling_price, min_order_qty
ITEMS = [
    ("SUGAR-001", "Sugar Refined (50 Kg Bag)", "Grocery & Staples", "Kg", 38.0, 42.0, 500),
    ("RICE-001", "Rice Basmati (25 Kg Bag)", "Grocery & Staples", "Kg", 65.0, 72.0, 250),
    ("FLOUR-001", "Wheat Flour (25 Kg Bag)", "Grocery & Staples", "Kg", 28.0, 32.0, 250),
    ("SALT-001", "Iodized Salt (1 Kg Pack)", "Grocery & Staples", "Kg", 8.0, 10.0, 200),
    ("PULSES-001", "Toor Dal (25 Kg Bag)", "Grocery & Staples", "Kg", 90.0, 100.0, 250),
    ("CHANA-001", "Chana Dal (25 Kg Bag)", "Grocery & Staples", "Kg", 75.0, 85.0, 250),

    ("OIL-001", "Sunflower Oil (15 Ltr Tin)", "Spices & Condiments", "Litre", 130.0, 145.0, 100),
    ("GHEE-001", "Desi Ghee (15 Kg Tin)", "Spices & Condiments", "Kg", 480.0, 530.0, 50),

    ("TEA-001", "Tea Leaves CTC (25 Kg Bag)", "Beverages", "Kg", 220.0, 250.0, 100),
    ("COFFEE-001", "Instant Coffee (1 Kg Jar)", "Beverages", "Kg", 380.0, 420.0, 50),

    ("BISCUIT-001", "Glucose Biscuit (1 Doz Box)", "Household", "Box", 55.0, 65.0, 48),

    ("SOAP-001", "Bathing Soap Bar (12 Nos Box)", "Personal Care", "Box", 90.0, 105.0, 24),
    ("DETERGENT-001", "Detergent Powder (1 Kg Pack)", "Personal Care", "Kg", 55.0, 65.0, 50),
    ("SHAMPOO-001", "Shampoo (200 ml Bottle)", "Personal Care", "Nos", 80.0, 95.0, 24),
    ("TOOTHPASTE-001", "Toothpaste (150 gm Tube)", "Personal Care", "Nos", 45.0, 55.0, 24),
]


# ─── Utilities ────────────────────────────────────────────────────────────────

def safe_insert(doc):
    doc.flags.ignore_permissions = True
    doc.flags.ignore_mandatory = True
    doc.insert(ignore_if_duplicate=True)


# ─── Setup Functions ──────────────────────────────────────────────────────────

def set_global_defaults():
    frappe.db.set_default("country", "India")
    frappe.db.set_default("currency", "INR")

    try:
        gd = frappe.get_single("Global Defaults")
        gd.default_currency = "INR"
        gd.country = "India"
        gd.save(ignore_permissions=True)
    except Exception:
        pass


def create_uoms():
    uoms = ["Kg", "Litre", "Box", "Nos"]

    for uom in uoms:
        if frappe.db.exists("UOM", uom):
            continue

        doc = frappe.get_doc({
            "doctype": "UOM",
            "uom_name": uom
        })

        safe_insert(doc)


def create_item_groups():
    parent = frappe.db.get_value(
        "Item Group",
        {"is_group": 1},
        "name"
    ) or "All Item Groups"

    for grp in ITEM_GROUPS:
        if frappe.db.exists("Item Group", grp):
            continue

        doc = frappe.get_doc({
            "doctype": "Item Group",
            "item_group_name": grp,
            "parent_item_group": parent,
            "is_group": 0,
        })

        safe_insert(doc)


def create_supplier_groups():
    for grp in SUPPLIER_GROUPS:
        if frappe.db.exists("Supplier Group", grp):
            continue

        doc = frappe.get_doc({
            "doctype": "Supplier Group",
            "supplier_group_name": grp,
        })

        safe_insert(doc)


def create_customer_groups():
    parent = frappe.db.get_value(
        "Customer Group",
        {"is_group": 1},
        "name"
    ) or "All Customer Groups"

    for grp in CUSTOMER_GROUPS:
        if frappe.db.exists("Customer Group", grp):
            continue

        doc = frappe.get_doc({
            "doctype": "Customer Group",
            "customer_group_name": grp,
            "parent_customer_group": parent,
            "is_group": 0,
        })

        safe_insert(doc)


def create_suppliers():
    for s in SUPPLIERS:
        if frappe.db.exists("Supplier", s["supplier_name"]):
            continue

        doc = frappe.get_doc({
            "doctype": "Supplier",
            "supplier_name": s["supplier_name"],
            "supplier_group": s["supplier_group"],
            "country": s["country"],
            "supplier_type": "Company",
        })

        safe_insert(doc)


def create_customers():
    for c in CUSTOMERS:
        if frappe.db.exists("Customer", c["customer_name"]):
            continue

        doc = frappe.get_doc({
            "doctype": "Customer",
            "customer_name": c["customer_name"],
            "customer_group": c["customer_group"],
            "customer_type": "Company",
            "territory": c["territory"],
        })

        safe_insert(doc)


def create_items():
    for (
        code,
        name,
        group,
        uom,
        buy_price,
        sell_price,
        moq,
    ) in ITEMS:

        if frappe.db.exists("Item", code):
            continue

        doc = frappe.get_doc({
            "doctype": "Item",
            "item_code": code,
            "item_name": name,
            "item_group": group,
            "stock_uom": uom,
            "is_purchase_item": 1,
            "is_sales_item": 1,
            "is_stock_item": 1,
            "description": name,
        })

        safe_insert(doc)


def create_item_prices():
    for (
        code,
        name,
        group,
        uom,
        buy_price,
        sell_price,
        moq,
    ) in ITEMS:

        if not frappe.db.exists("Item", code):
            continue

        for price_list, rate in [
            ("Standard Buying", buy_price),
            ("Standard Selling", sell_price),
        ]:

            exists = frappe.db.exists(
                "Item Price",
                {
                    "item_code": code,
                    "price_list": price_list,
                }
            )

            if exists:
                continue

            doc = frappe.get_doc({
                "doctype": "Item Price",
                "item_code": code,
                "price_list": price_list,
                "price_list_rate": rate,
                "currency": "INR",
            })

            safe_insert(doc)


def link_items_to_suppliers():
    supplier_item_map = {
        s["supplier_name"]: s["items"]
        for s in SUPPLIERS
    }

    for supplier_name, item_codes in supplier_item_map.items():

        if not frappe.db.exists("Supplier", supplier_name):
            continue

        for item_code in item_codes:

            if not frappe.db.exists("Item", item_code):
                continue

            exists = frappe.db.exists(
                "Item Supplier",
                {
                    "parent": item_code,
                    "supplier": supplier_name,
                }
            )

            if exists:
                continue

            item = frappe.get_doc("Item", item_code)

            item.append(
                "supplier_items",
                {
                    "supplier": supplier_name
                }
            )

            item.flags.ignore_permissions = True
            item.flags.ignore_mandatory = True
            item.save()


# ─── Main Entry Point ─────────────────────────────────────────────────────────

def create_demo_data():

    frappe.flags.in_setup = True

    steps = [
        ("Global Defaults", set_global_defaults),
        ("UOMs", create_uoms),
        ("Item Groups", create_item_groups),
        ("Supplier Groups", create_supplier_groups),
        ("Customer Groups", create_customer_groups),
        ("Suppliers", create_suppliers),
        ("Customers", create_customers),
        ("Items", create_items),
        ("Item Prices", create_item_prices),
        ("Supplier Item Links", link_items_to_suppliers),
    ]

    for label, fn in steps:

        try:
            fn()
            frappe.db.commit()
            print(f"✓ {label}")

        except Exception as e:
            frappe.db.rollback()
            frappe.log_error(
                frappe.get_traceback(),
                f"Smart Market Setup Error - {label}"
            )

            print(f"✗ {label}: {str(e)}")

    frappe.flags.in_setup = False

    print("Smart Market demo data setup completed.")
