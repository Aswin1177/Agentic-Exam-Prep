import pymupdf
def load_printed_pdf(pdf_files):
    if isinstance(pdf_files, str):
        pdf_files = [pdf_files]
    full_txt = []
    for pdf in pdf_files:
        print(f"loading {pdf} ...", flush=True)
        doc = pymupdf.open(pdf)
        for i, page in enumerate(doc):
            text = page.get_text("text")
            full_txt.append(text)
        print(f"{pdf} completed", flush=True)

    print(f"Loaded {len(pdf_files)} PDF(s) successfully")
    return full_txt



def load_hw_pdf(pdf_files):
    from pdf2image import convert_from_path
    from paddleocr import PaddleOCR
    import numpy as np
    ocr = PaddleOCR(use_angle_cls=True,lang="en")
    if isinstance(pdf_files, str):
        pdf_files = [pdf_files]
    full_text = []
    for pdf in pdf_files:
        print("loading",pdf,"...")
        images = convert_from_path(pdf)
        for image in images:
            image_arr=np.array(image)
            result = ocr.predict(input=image_arr)
            page_text = []
            for line in result[0]:
                page_text.append(line[1][0])
            full_text.append("\n".join(page_text))

    print(f"OCR extraction completed for {len(pdf_files)} PDF(s)")
    return full_text
