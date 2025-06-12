
import frappe

@frappe.whitelist()
def calculate_emissions():
    # Static dummy calculation for demo
    return "Estimated Emissions: 9000 kg CO₂e (3 floors, 3 bedrooms)"
