import streamlit as st
import os
from graph.workflow import run_workflow

st.title("Exam Prep AI")

qpprs=st.file_uploader("Upload Previous Year Question Papers",type=["pdf"],accept_multiple_files=True)

notes=st.file_uploader("Upload Notes PDFs",type=["pdf"],accept_multiple_files=True)

if st.button("Generate Focused Notes"):

    if not qpprs or not notes:
        st.error("Please upload both question papers and notes.")
        st.stop()

    os.makedirs("uploads/qpprs",exist_ok=True)
    os.makedirs("uploads/notes",exist_ok=True)

    qppr_files=[]

    for file in qpprs:
        path=f"uploads/qpprs/{file.name}"

        with open(path,"wb") as f:
            f.write(file.getbuffer())

        qppr_files.append(path)

    notes_files=[]

    for file in notes:
        path=f"uploads/notes/{file.name}"

        with open(path,"wb") as f:
            f.write(file.getbuffer())

        notes_files.append(path)

    with st.spinner("Generating focused notes..."):
        result=run_workflow(
            qppr_files=qppr_files,
            notes_files=notes_files,
            handwritten=False
        )

    st.success("Notes Generated")
    st.subheader("Focused Notes")
    st.write(result["focused_notes"])