import streamlit as st
import PyPDF2
from google import genai

# ---------------- GEMINI API SETUP ----------------

API_KEY = "AIzaSyDOm0zO4sYz_YKPYuc6djVKXmcHXdh_jXQ"

client = genai.Client(api_key=API_KEY)

# ---------------- PDF TEXT EXTRACTION ----------------

def extract_text_from_pdf(pdf_file):

    text = ""

    reader = PyPDF2.PdfReader(pdf_file)

    for page in reader.pages:

        extracted = page.extract_text()

        if extracted:
            text += extracted

    return text

# ---------------- TEXT CHUNKING ----------------
#without overlap
# def split_text(text, chunk_size=500):

#     chunks = []

#     for i in range(0, len(text), chunk_size):

#         chunks.append(text[i:i + chunk_size])

#     return chunks

def split_text(text, chunk_size=400, overlap=75):

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end]

        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks

# ---------------- KEYWORD SEARCH ----------------

def search_chunks(question, chunks):

    relevant_chunks = []

    question_words = question.lower().split()

    for chunk in chunks:

        chunk_lower = chunk.lower()

        for word in question_words:

            if word in chunk_lower:

                relevant_chunks.append(chunk)

                break

    return relevant_chunks[:3]

# ---------------- GEMINI RESPONSE ----------------

def ask_gemini(question, context):

    prompt = f"""

    Answer the question only from the given PDF context.

    Context:
    {context}

    Question:
    {question}
    """

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )

    return response.text

# ---------------- STREAMLIT UI ----------------

st.title("PDF Chatbot using Gemini New SDK")

uploaded_file = st.file_uploader(
    "Upload PDF",
    type="pdf"
)

if uploaded_file is not None:

    # Extract text
    pdf_text = extract_text_from_pdf(uploaded_file)

    # Split into chunks
    chunks = split_text(pdf_text)

    st.success("PDF Loaded Successfully!")

    # Ask question
    question = st.text_input("Ask Question from PDF")

    if question:

        # Search relevant chunks
        relevant_chunks = search_chunks(question, chunks)

        # Combine chunks
        context = " ".join(relevant_chunks)

        # Get Gemini answer
        answer = ask_gemini(question, context)

        # Display answer
        st.subheader("Answer")

        st.write(answer)