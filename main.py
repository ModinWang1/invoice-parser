import os
from reader import process_invoice
from parse_output import parse_output
from csv_writer import write_to_csv

prompt = (
    "You are a data extraction assistant.\n\n"
    "Task:\n"
    "Extract the following fields from the invoice or receipt image:\n"
    "- 'invoice_number': string ('N/A' if missing)\n"
    "- 'date': string in mm/dd/yyyy format ('N/A' if missing)\n"
    "- 'items': a list of dictionaries, each with 'name', 'quantity', and 'cost'\n"
    "- 'subtotal': number (0.0 if missing)\n"
    "- 'tax': number (0.0 if missing)\n"
    "- 'total': number (0.0 if missing)\n\n"
    "Only return a valid Python dictionary with **all** of these keys. No extra text.\n\n"
    "Example format (do not copy values):\n"
    "{\n"
    "  'invoice_number': <string>,\n"
    "  'date': <mm/dd/yyyy>,\n"
    "  'items': [{'name': <string>, 'quantity': <int>, 'cost': <float>}],\n"
    "  'subtotal': <float>,\n"
    "  'tax': <float>,\n"
    "  'total': <float>\n"
    "}\n\n"
    "Now extract the values from the current image. "
    "Keep in mind, if there is no quantity on an item it is assumed to be 1. "
    "Also keep in mind that tax can also be known as GST or HST. "
    "Also keep in mind that the 'total' is usually the largest amount and should at least be the same as the subtotal. "
    "Also keep in mind 'invoice number' can also be known as 'invoice #'"
)
all_data = []
folder_path = "./invoices"

for filename in os.listdir(folder_path):
    if filename.endswith(('.jpg', '.png', '.jpeg', '.webp')):
        full_path = os.path.join(folder_path, filename)
        print(f"Processing {filename}...")
        response = process_invoice(full_path, prompt)
        parsed = parse_output(response)
        parsed['filename'] = filename  # optional for traceability
        all_data.append(parsed)

# Adjust fieldnames based on your schema
fieldnames = ['filename', 'invoice_number', 'date', 'subtotal', 'tax', 'total_amount_due']
write_to_csv("output.csv", all_data, fieldnames)