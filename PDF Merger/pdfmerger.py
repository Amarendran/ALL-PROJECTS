import pypdf
from pypdf import PdfMerger

#pdfs = ['file1.pdf', 'file2.pdf', 'file3.pdf', 'file4.pdf']
pdfs = ['1_HDFC_CHECK.pdf', '2_HDFC_STATEMENT.pdf']

merger = PdfMerger()

for pdf in pdfs:
    merger.append(pdf)

merger.write("result.pdf")
merger.close()