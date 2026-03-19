import frappe


def daily():
    """Daily scheduled tasks"""
    # Check for overdue opportunities
    check_overdue_opportunities()


def check_overdue_opportunities():
    """Flag opportunities past their expected closing date"""
    from frappe.utils import today

    overdue = frappe.get_all(
        "Opportunity",
        filters={
            "status": "Open",
            "expected_closing": ["<", today()],
        },
        fields=["name", "title", "opportunity_owner"],
    )

    for opp in overdue:
        frappe.publish_realtime(
            "overdue_opportunity",
            {"name": opp.name, "title": opp.title},
            user=opp.opportunity_owner,
        )
