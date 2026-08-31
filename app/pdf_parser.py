from pypdf import PdfReader


def extract_text_from_pdf(uploaded_file):
    """Extract text from an uploaded PDF resume."""

    reader = PdfReader(uploaded_file)

    extracted_text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            extracted_text += page_text + "\n"

    return extracted_text.strip()
import streamlit as st
from pdf_parser import extract_text_from_pdf
from pypdf import PdfReader


def extract_text_from_pdf(uploaded_file):
    """Extract text from an uploaded PDF resume."""

    reader = PdfReader(uploaded_file)

    extracted_text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            extracted_text += page_text + "\n"

    return extracted_text.strip()