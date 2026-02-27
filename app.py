import streamlit as st
import fitz  # PyMuPDF

st.set_page_config(page_title="PDF Scrub", page_icon="⚖️")
st.title("Watermark Remover Test App")
st.write("Upload your PDF to identify and remove background watermarks.")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file:
    # Open the PDF from the upload
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    
    # Show user what images are on Page 1 to find the IDs
    st.subheader("1. Identify Your Watermark")
    st.info("Check the IDs below. The watermark is usually the largest image.")
    
    images = doc[0].get_images(full=True)
    cols = st.columns(3)
    for i, img in enumerate(images):
        xref = img[0]
        with cols[i % 3]:
            st.write(f"**ID: {xref}**")
            st.caption(f"Size: {img[2]}x{img[3]}")

    # Removal Section
    st.subheader("2. Remove and Download")
    ids_to_remove = st.text_input("Enter IDs to delete (e.g., 3847, 3848)")

    if st.button("Clean My PDF") and ids_to_remove:
        target_ids = [int(x.strip()) for x in ids_to_remove.split(",")]
        
        for page in doc:
            for tid in target_ids:
                page.delete_image(tid)
        
        output_bytes = doc.write()
        st.success("Cleaned!")
        st.download_button("Download Cleaned PDF", output_bytes, f"cleaned_{uploaded_file.name}")
