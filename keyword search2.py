import PyPDF2
from google import genai
from google.genai import types
# ---------------- GEMINI API SETUP ----------------

API_KEY = "your gemini api key"

# Create Gemini client
client = genai.Client(api_key=API_KEY)

# ---------------- PDF TEXT EXTRACTION ----------------

def extract_text(pdf_path):

    text = ""

    with open(pdf_path, "rb") as file:

        reader = PyPDF2.PdfReader(file)

        for page in reader.pages:

            extracted = page.extract_text()

            if extracted:
                text += extracted

    return text

# ---------------- TEXT CHUNKING ----------------

def split_text(text, chunk_size=500):

    chunks = []

    for i in range(0, len(text), chunk_size):

        chunks.append(text[i:i + chunk_size])

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
    You are a PDF assistant.
    Answer the question only from the given PDF context.

    Context:
    {context}

    Question:
    {question}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        #config=types.GenerateContentConfig(
            # #Controls randomness/creativity of output.
            # #High temp leads to more creative,more random,sometimes hallucinations
            # temperature=0.3,
            # #Probability threshold
            # top_p=0.8,
            # #Fixed number of words
            # top_k=20,
            # #Controls maximum response length.
            # #max_output_tokens=300,
            # #Number of responses generated.
            # candidate_count=1,
            # #Stops generation when model encounters specified text.
            # stop_sequences=["END"],
            # # Encourages model to talk about new topics.
            # # if the value is higher Model avoids repeating same concepts.
            # presence_penalty=0.0,
            # #Reduces repeated words/phrases.
            # #if the value is higher this Avoids repeating same words again and again.
            # frequency_penalty=0.0
        #)
    )

    return response.text

# ---------------- MAIN PROGRAM ----------------

print("PDF Chatbot Using Gemini")

# Enter PDF path
pdf_path = input("\nEnter PDF path: ")

# Extract text
pdf_text = extract_text(pdf_path)

# Split into chunks
chunks = split_text(pdf_text)

print("\nPDF Loaded Successfully!")

# Chat loop
while True:

    question = input("\nAsk Question (type 'exit' to stop): ")

    if question.lower() == "exit":
        print("\nChatbot Closed")
        break

    # Search relevant chunks
    relevant_chunks = search_chunks(question, chunks)

    # Combine chunks
    context = " ".join(relevant_chunks)

    # Ask Gemini
    answer = ask_gemini(question, context)

    # Print answer
    print("\nAnswer:")
    print(answer)