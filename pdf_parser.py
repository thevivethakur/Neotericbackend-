
import frappe
import fitz  # PyMuPDF

@frappe.whitelist()
def parse_pdf(file_url):
    path = frappe.get_site_path('public', file_url.replace('/files/', ''))
    doc = fitz.open(path)
    text = ""
    for page in doc:
        text += page.get_text()
    results = [line for line in text.splitlines() if "cement" in line.lower()]
    return "\n".join(results)
