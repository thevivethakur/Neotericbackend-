
import frappe

@frappe.whitelist()
def calculate_emissions():
    return "Estimated Emissions: 9000 kg CO₂e"
