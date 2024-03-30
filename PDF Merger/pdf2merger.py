from PyPDF2 import PdfMerger #PyPDF2

pdfs = ['0_Scanned_Document.pdf','1_HDFC_CHECK.pdf', '2_HDFC_STATEMENT.pdf','3_PASSPORT.pdf','4_Pan_card.pdf','5_Adhaar.pdf','6_EPFO_UAN.pdf','7_FORM16_1.pdf','7_FORM16_2.pdf','8_EGIL16328_FNF.pdf']
merger = PdfMerger()

for pdf in pdfs:
    merger.append(pdf)

merger.write("result.pdf")
merger.close()
