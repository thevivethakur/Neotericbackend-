
import frappe
import openai

@frappe.whitelist()
def ask_chatgpt(prompt):
    openai.api_key = frappe.conf.get("openai_api_key")
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message['content']
