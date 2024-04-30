from mpi4py import MPI
import fitz
from sys import argv

# Function to distribute pages evenly across processes
def distribute_pages(pdf_file, num_processes):
    num_pages = len(fitz.open(pdf_file))
    pages_per_process = num_pages // num_processes
    remainder = num_pages % num_processes
    
    # Calculate start and end page for each process
    start_page = 0
    for rank in range(num_processes):
        end_page = start_page + pages_per_process - 1
        if rank < remainder:
            end_page += 1
        yield (start_page, end_page)
        start_page = end_page + 1

if __name__ == "__main__":
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    if len(argv) != 2:
        if rank == 0:
            print(f"Usage: {argv[0]} <pdf_file>")
        exit()

    pdf_file = argv[1]

    if rank == 0:
        print(f"Number of processes: {size}")

    # Distribute pages among processes
    page_range = list(distribute_pages(pdf_file, size))

    # Each process opens the PDF and extracts its pages
    start_page, end_page = page_range[rank]
    extracted_pages = []
    with fitz.open(pdf_file) as doc:
        for page_number in range(start_page, end_page + 1):
            page = doc.load_page(page_number)
            extracted_pages.append(page)

    print(f"Process {rank} extracted {len(extracted_pages)} pages: pages {start_page} to {end_page}")

    # Now you can perform further processing with the extracted pages in each process