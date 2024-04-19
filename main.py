import fitz

# Define a function to find images in a PDF file
def find_images(pdf_file):
    # Open the PDF file using PyMuPDF
    with fitz.open(pdf_file) as doc:
        # Iterate through each page in the PDF document
        for page_index, page in enumerate(doc):
            # Iterate through each image on the page
            for img in page.get_images():
                # Get the image reference (xref)
                xref = img[0]
                # Extract the image metadata
                base_image = doc.extract_image(xref)
                # Print a message to the console indicating that an image was found
                print(f"Image Found on Page: {page_index+1}")
                # Uncomment the following line to print the image metadata
                # print(f"Image metadata: {base_image}")

# Call the function with the PDF file path
find_images("data/390.pdf")