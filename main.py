import warnings
warnings.filterwarnings("ignore")
import streamlit as st
import os
os.makedirs("uploads", exist_ok=True)
os.makedirs("vectorstores", exist_ok=True)
from graph.notes_workflow import run_notes_workflow
from graph.revision_workflow import run_revision_workflow
from graph.mock_workflow import run_mock_workflow
from pdf_generator import create_notes_pdf,create_revision_pdf,create_mock_pdf
from dotenv import load_dotenv
load_dotenv()

st.title("Exam Preperation AI")

qpprs=st.file_uploader("Upload Previous Year Question Papers",type=["pdf"],accept_multiple_files=True)

def save_uploaded_files(files,folder):

    os.makedirs(folder,exist_ok=True)

    paths=[]

    for file in files:

        path=f"{folder}/{file.name}"

        with open(path,"wb") as f:
            f.write(file.getbuffer())

        paths.append(path)

    return paths


st.divider()

st.subheader("Focused Notes Generator")

notes=st.file_uploader("Upload Notes PDFs",type=["pdf"],accept_multiple_files=True,key="notes")

if st.button("Generate Focused Notes"):

    if not qpprs or not notes:
        st.error("Please upload question papers and notes.")
        st.stop()

    qppr_files=save_uploaded_files(qpprs,"uploads/qpprs")
    notes_files=save_uploaded_files(notes,"uploads/notes")

    with st.spinner("Generating focused notes..."):

        result=run_notes_workflow(
            qppr_files=qppr_files,
            notes_files=notes_files,
            handwritten=False
        )

    pdf_path=create_notes_pdf(result["focused_notes"])

    st.success("Focused Notes Generated")

    with open(pdf_path,"rb") as pdf_file:

        st.download_button(
            label="Download Focused Notes PDF",
            data=pdf_file,
            file_name="Focused_Notes.pdf",
            mime="application/pdf"
        )

st.divider()

st.subheader("Revision Planner")

syllabus=st.file_uploader("Upload Syllabus PDF",type=["pdf"],key="syllabus")

days_to_exam=st.number_input("Days Until Exam",min_value=1,value=14)

hours_per_day=st.number_input("Study Hours Per Day",min_value=1,max_value=16,value=4)

if st.button("Generate Revision Plan"):

    if not qpprs:
        st.error("Please upload question papers.")
        st.stop()

    if syllabus is None:
        st.error("Please upload syllabus PDF.")
        st.stop()

    qppr_files=save_uploaded_files(qpprs,"uploads/qpprs")

    os.makedirs("uploads/syllabus",exist_ok=True)

    syllabus_path=f"uploads/syllabus/{syllabus.name}"

    with open(syllabus_path,"wb") as f:
        f.write(syllabus.getbuffer())

    with st.spinner("Generating revision plan..."):

        result=run_revision_workflow(
            qppr_files=qppr_files,
            syllabus_file=syllabus_path,
            days_to_exam=days_to_exam,
            hours_per_day=hours_per_day
        )

    pdf_path=create_revision_pdf(result["revision_plan"])

    st.success("Revision Plan Generated")

    with open(pdf_path,"rb") as pdf_file:

        st.download_button(
            label="Download Revision Plan PDF",
            data=pdf_file,
            file_name="Revision_Plan.pdf",
            mime="application/pdf"
        )

st.divider()

st.subheader("Mock Examiner")

st.caption("Upload at least one question paper. The first paper will be used as the reference pattern.")

if st.button("Generate Mock Test Paper"):

    if not qpprs:
        st.error("Please upload at least one question paper.")
        st.stop()

    qppr_files=save_uploaded_files(qpprs,"uploads/qpprs")

    with st.spinner("Generating mock question paper..."):

        result=run_mock_workflow(
            qppr_files=qppr_files
        )

    pdf_path=create_mock_pdf(result["mock_test"])

    st.success("Mock Test Paper Generated")

    with open(pdf_path,"rb") as pdf_file:

        st.download_button(
            label="Download Mock Test PDF",
            data=pdf_file,
            file_name="Mock_Test_Paper.pdf",
            mime="application/pdf"
        )