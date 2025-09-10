import streamlit as st
from PyPDF2 import PdfReader, PdfWriter
import io
import zipfile

st.title("Patient PDF Splitter")

# Upload PDF
uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file:
    reader = PdfReader(uploaded_file)
    num_pages = len(reader.pages)
    
    # Keyword that marks the end of a patient report
    keyword = st.text_input("Enter the keyword that marks the end of a patient report (e.g., 'End of Report'):")

    if keyword:
        patient_count = 0
        writer = PdfWriter()
        patient_pdfs = []

        for i, page in enumerate(reader.pages):
            text = page.extract_text() or ""
            writer.add_page(page)

            # If the keyword is found or last page, save current patient PDF
            if keyword.lower() in text.lower() or i == num_pages - 1:
                patient_count += 1
                pdf_bytes = io.BytesIO()
                writer.write(pdf_bytes)
                pdf_bytes.seek(0)
                patient_pdfs.append((f"patient_{patient_count}.pdf", pdf_bytes.read()))
                writer = PdfWriter()  # Reset for next patient

        # Create a ZIP file with all patient PDFs
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
            for file_name, data in patient_pdfs:
                zip_file.writestr(file_name, data)
        zip_buffer.seek(0)

        # Download button for the ZIP
        st.download_button(
            label=f"Download All {patient_count} Patient PDFs",
            data=zip_buffer.getvalue(),
            file_name="all_patients.zip",
            mime="application/zip"
        )

        st.success(f"Split completed! Total patients: {patient_count}")
