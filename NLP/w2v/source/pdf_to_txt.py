'''
import PyPDF2 as pyPdf

filename = "intro_to_envi.pdf";
pdf = pyPdf.PdfFileReader(open(filename, "rb"))
i = -1;
for page in pdf.pages:
    i = i + 1;
    print("---Page ", i, ":--------------------------------");
    print (page.extractText())
    
    input("Press Enter to continue...")
    
'''

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO

    
import os

######################
## Find all pdfs
#########################
root = "pdfs";
pdf_list = [];
i = -1;
for afile in os.listdir(root):
    if afile.endswith(".pdf"):
        i = i+1;
        pdf_list.append(afile);
        #print(file)
#print (pdf_list);
#exit();


def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = file(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    try:
        for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching):
            interpreter.process_page(page)
        text = retstr.getvalue()
    except Exception:
        text = "Text Not Extractable";
        pass

    fp.close()
    device.close()
    retstr.close()
    return text

######################
## Convert all pdfs
#########################
print("\n");
print("Converting all pdfs...");
for file_name in pdf_list:
    #file_name = "lonely_planet.pdf";
    file_path = root + "/" + file_name;
    print (" -- Converting " + file_path);
    text = convert_pdf_to_txt(file_path);
    #print(text);

    f = open("txt/"+file_name[0:-3]+'.txt', 'w+')
    f.write(text);  # python will convert \n to os.linesep
    f.close()  # you can omit in most cases as the destructor will call it


