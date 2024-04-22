import fitz
import os
import sqlite3

def extract_figure_captions(txt_file):
    with open(txt_file, "r") as file:
        caption = []
        for line in file:
            line = line.strip()
            if line.startswith("Figure"):
                caption.append(line)
            elif line.startswith("Fig."):
                yield line
            elif caption and line:  # continue adding lines to the caption
                caption.append(line)
            elif caption and not line:  # empty line indicates end of caption
                yield " ".join(caption)
                caption = []
        if caption:  # yield the last caption
            yield " ".join(caption)

# Define a function to find images in a PDF file
def find_images(pdf_file, output_dir, db_file):
    # Create the "pages" folder if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Open the PDF file using PyMuPDF
    with fitz.open(pdf_file) as doc:
        # Create a connection to the database
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        
        # Create a table for the figure data if it doesn't exist
        c.execute('''CREATE TABLE IF NOT EXISTS figures
                     (page INTEGER, caption TEXT)''')
        
        # Iterate through each page in the PDF document
        for page_index, page in enumerate(doc):
            # Get the text of the page
            page_text = page.get_text()
            # Export the text to a separate txt file in the "pages" folder
            with open(f"{output_dir}/page_{page_index+1}.txt", "w") as txt_file:
                txt_file.write(page_text)
            # Iterate through each image on the page
            for img in page.get_images():
                # Get the image reference (xref)
                xref = img[0]
                # Extract the image metadata
                base_image = doc.extract_image(xref)
                # Print a message to the console indicating that an image was found
                print(f"Image Found on Page: {page_index+1}")
                # Extract figure captions from the page text
                figure_captions = extract_figure_captions(f"{output_dir}/page_{page_index+1}.txt")
                for caption in figure_captions:
                    print(f"Page {page_index+1}: {caption}")
                    # Insert the figure data into the database
                    c.execute("INSERT INTO figures VALUES (?, ?)",
                              (page_index+1, caption))
        # Commit the changes and close the connection
        conn.commit()
        conn.close()

# Call the function with the PDF file path, output directory, and database file
find_images("data/390.pdf", "pages", "figures.db")