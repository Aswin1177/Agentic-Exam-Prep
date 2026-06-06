import pymupdf 
def load_pdf(pdf):
    doc=pymupdf.open(pdf)   
    full_txt=[]
    for page in doc:
        full_txt.append(page.get_text("text"))
    print("PDF loaded successfully")
    return full_txt
