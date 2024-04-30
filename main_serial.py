import fitz
from sys import argv
from timeit import default_timer as timer
from typing import List

# Importing PageData class from your script
from page_data import PageData 

def extract_figures_from_pdf(pdf_file: str) -> List[str]:
    """
    Extract figure captions from all pages of a PDF file.
    
    Args:
    - pdf_file (str): Path to the PDF file.
    
    Returns:
    - List[str]: List of figure captions extracted from the PDF.
    """
    figure_captions = []
    
    with fitz.open(pdf_file) as doc:
        for page_number in range(len(doc)):
            page_data = PageData(doc[page_number], page_number)
            figure_captions.extend(page_data.fig_capts)
    
    return figure_captions

if __name__ == "__main__":
    if len(argv) != 2:
        print(f"Usage: {argv[0]} <pdf_file>")
    else:
        pdf_file_path = argv[1]
        figure_captions = extract_figures_from_pdf(pdf_file_path)
        print("Extracted Figures:")
        for idx, caption in enumerate(figure_captions, start=1):
            print(f"Figure {idx}: {caption}")
