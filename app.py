import streamlit as st
from PIL import Image
from reader import process_invoice
from image_processing import preprocess_invoice_image
import os

# Ensure that the 'temp' folder exists
if not os.path.exists("temp"):
    os.makedirs("temp")

st.title("🧾 Invoice Parser")

# File uploader widget to upload multiple invoice images
uploaded_files = st.file_uploader("Upload one or more invoice images", accept_multiple_files=True, type=["png", "jpg", "jpeg", "webp"])

prompt = (
    "Extract the following info from the invoice or receipt:\n"
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

"""
prompt = (
    "Extract the invoice number, date, items (a list of dictionaries, each with 'name', 'quantity', and 'cost'), subtotal, tax, and total from the invoice or receipt:\n"
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
    "Keep in mind, if there is no quantity on an item it is assumed to be 1. "
    "Note: 'invoice number' may be labeled as 'Invoice #', 'Ref No.', or 'Bill No.' 'Tax' may be labeled as GST/HST/VAT. 'Total' is usually the largest number and includes tax."
    "Return only a valid JSON-formatted Python dictionary with these keys: [...]. Do not include explanations or extra text. All monetary values should be floats rounded to two decimal places. Item quantities must be integers. Dates must follow mm/dd/yyyy. If any value is missing, return a fallback ('N/A' or 0.0)."
)
"""
if uploaded_files:
    for uploaded_file in uploaded_files:
        # Display the uploaded image for preview
        st.image(uploaded_file, caption=f"Preview: {uploaded_file.name}", use_column_width=True)

        # Read the image file from the uploader
        image = Image.open(uploaded_file).convert("RGB")

        # Save the uploaded file to the temp folder
        temp_path = os.path.join("temp", uploaded_file.name)
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Process the saved image file using the full path
        with st.spinner(f"Processing {uploaded_file.name}..."):
            try:
                result = process_invoice(temp_path, prompt)
                st.success("Extracted Data:")
                st.write(result)
            except Exception as e:
                st.error(f"Error processing {uploaded_file.name}: {str(e)}")
