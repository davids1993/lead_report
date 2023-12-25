import PyPDF2
from xhtml2pdf import pisa
from PyPDF2 import PdfMerger


# use xhtml2pdf to convert html to pdf 
# need to paginate the html by fitting the html between the header and footer
# need to create a template pdf with the header and footer
# add a page number to the footer
# include project info in the header

# merge multiple pdfs into one
def merge_pdfs(pdf_list, output):
    merger = PyPDF2.PdfMerger()
    for pdf in pdf_list:
        merger.append(pdf)
        
    merger.write(output)
    merger.close()
    
    
# merge_pdfs(["C:\\Users\\dovid\\OneDrive\\Downloads\\Report.pdf", "C:\\Users\\dovid\\OneDrive\\Downloads\\Aristacare___Cedar_Oaks___Steam_Table.pdf"], "C:\\Users\\dovid\\OneDrive\\Downloads\\Report2.pdf")



# Utility function
def convert_html_to_pdf(source_html, output_filename, encoding='utf-8'):
    # open output file for writing (truncated binary)
    result_file = open(output_filename, "w+b")

    # convert HTML to PDF
    pisa_status = pisa.CreatePDF(
            source_html,                # the HTML to convert
            dest=result_file)           # file handle to recieve result

    # close output file
    result_file.close()                 # close output file

    # return False on success and True on errors
    return pisa_status.err

