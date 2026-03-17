from . import __version__ as app_version

app_name = "wsapp"
app_title = "WS App"
app_publisher = "Your Company"
app_description = "ERP/CRM System based on Frappe Framework"
app_email = "your@email.com"
app_license = "MIT"

# Apps
# ------------------
# required_apps = []

# Each item in the list will be shown as an app in the apps page
add_to_apps_screen = [
    {
        "name": "wsapp",
        "logo": "/assets/wsapp/images/logo.png",
        "title": "WS App",
        "route": "/wsapp",
        "has_permission": "wsapp.api.permission.has_app_permission",
    }
]

# Includes in <head>
# ------------------
# include_js = {"page" :  "public/js/file.js"}
# include_css = {"page" : "public/css/file.css"}
# include_script = {"page" : "public/js/file.js"}

# Home Pages
# ----------
home_page = "login"

# Generators
# ----------
# website_generators = ["Web Page"]

# Jinja
# ----------
# jinja = {
#     "methods": "wsapp.utils.jinja_methods",
#     "filters": "wsapp.utils.jinja_filters",
# }

# Installation
# ------------
before_install = "wsapp.setup.install.before_install"
after_install = "wsapp.setup.install.after_install"

# Uninstallation
# ------------
# before_uninstall = "wsapp.setup.install.before_uninstall"
# after_uninstall = "wsapp.setup.install.after_uninstall"

# Integration Setup
# ------------------
# before_migrate = []
# after_migrate = []

# Desk Notifications
# ------------------
# get_notification_config = "wsapp.notifications.get_notification_config"

# Permissions
# -----------
# permission_query_conditions = {
#     "Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }

# Document Events
# ---------------
doc_events = {
    # "Customer": {
    #     "on_submit": "wsapp.crm.customer.on_submit",
    # }
}

# Scheduled Tasks
# ---------------
scheduler_events = {
    "daily": [
        "wsapp.tasks.daily",
    ],
}

# Testing
# -------
# before_tests = "wsapp.install.before_tests"

# Overriding Methods
# ------------------
# override_whitelisted_methods = {
#     "frappe.desk.doctype.event.event.get_permission_query_conditions": "wsapp.event.get_permission_query_conditions"
# }

# override class-based views by adding custom_domains to the workspace list
# override_doctype_class = {
#     "ToDo": "custom_app.overrides.CustomToDo"
# }

# Fixtures
# --------
fixtures = [
    {"dt": "Role", "filters": [["name", "in", ["CRM User", "CRM Manager", "ERP User", "ERP Manager"]]]},
]
