from RAG.loader import load_printed_pdf

pages = load_printed_pdf([
    "notes.pdf",
    "notes2.pdf",
    "notes3.pdf"
])

print("DONE")