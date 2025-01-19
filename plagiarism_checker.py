import streamlit as st
from difflib import SequenceMatcher
from PyPDF2 import PdfReader
import docx
import ollama

# Page Configuration
st.set_page_config(page_title="Plagiarism & Chatbot", layout="wide")

# Initialize Session State
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "user_input_buffer" not in st.session_state:
    st.session_state.user_input_buffer = ""
if "active_page" not in st.session_state:
    st.session_state.active_page = "Plagiarism Checker"  # Default page

# Functions
def calculate_similarity(text1, text2):
    """Calculate text similarity."""
    similarity = SequenceMatcher(None, text1, text2).ratio()
    return similarity * 100

def extract_text_from_pdf(uploaded_file):
    """Extract text from a PDF file."""
    pdf_reader = PdfReader(uploaded_file)
    return "".join(page.extract_text() for page in pdf_reader.pages)

def extract_text_from_word(uploaded_file):
    """Extract text from a Word file."""
    doc = docx.Document(uploaded_file)
    return "\n".join(paragraph.text for paragraph in doc.paragraphs)

def generate_response(user_input):
    try:
        # Prepare the conversation history for the prompt
        conversation_history = "\n".join(
            [f"{msg['role'].capitalize()}: {msg['content']}" for msg in st.session_state.chat_history]
        )
        
        # Prepare the prompt with conversation history
        prompt = (
            "You are a friendly and helpful chatbot designed to assist users with questions about plagiarism and plagiarism checking in NLP. "
            "Your primary goal is to educate users about plagiarism and plagiarism checking in NLP in a simple and clear manner. "
            "If the user greets you or initiates small talk, respond warmly but quickly steer the conversation back to plagiarism and plagiarism checking in NLP. "
            "If the user's query is related to plagiarism and plagiarism checking in NLP, provide a concise and accurate response. "
            "If the query is ambiguous or unclear, ask clarifying questions to better understand the user's needs. "
            "If the query is not related to plagiarism and plagiarism checking in NLP, respond with the following exact phrase: "
            "'I'm sorry, I specialize in helping with plagiarism-related topics. Let me know if you have any questions about plagiarism and plagiarism checking in NLP.!' "
            "Do not engage in off-topic discussions under any circumstances. "
            "Always maintain a friendly and supportive tone.\n\n"
            "Here is the conversation so far:\n"
            + conversation_history + "\n\n"
            f"User's latest question: {user_input}"
        )
        
        # Generate response with the guiding prompt
        response = ollama.generate(model="gemma2:2b", prompt=prompt)
        return response["response"]
    except Exception as e:
        return f"Error: {e}"

# Submit Message Function
def submit_message():
    user_input = st.session_state.user_input_buffer
    if user_input.strip():
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        response = generate_response(user_input)
        st.session_state.chat_history.append({"role": "bot", "content": response})
        st.session_state.user_input_buffer = ""  # Clear the buffer

# Sidebar: Navigation
with st.sidebar:
    st.markdown("### Navigation")
    # Sidebar options
    if st.button("Chatbot"):
        st.session_state.active_page = "Chatbot"
    if st.button("Plagiarism Checker"):
        st.session_state.active_page = "Plagiarism Checker"
    if st.button("Info about Plagiarism Checker"):
        st.session_state.active_page = "Info about Plagiarism Checker"

# Main Content
if st.session_state.active_page == "Plagiarism Checker":
    st.markdown("<h1 style='text-align: center;'>Plagiarism Checker</h1>", unsafe_allow_html=True)

    # Main Layout: Plagiarism Checker
    col1, col2 = st.columns(2)

    with col1:
        uploaded_file1 = st.file_uploader("Upload First File (PDF or Word)", type=["pdf", "docx"])
        if uploaded_file1:
            text1 = extract_text_from_pdf(uploaded_file1) if uploaded_file1.name.endswith(".pdf") else extract_text_from_word(uploaded_file1)
        else:
            text1 = st.text_area("Paste Text 1", height=200)

    with col2:
        uploaded_file2 = st.file_uploader("Upload Second File (PDF or Word)", type=["pdf", "docx"])
        if uploaded_file2:
            text2 = extract_text_from_pdf(uploaded_file2) if uploaded_file2.name.endswith(".pdf") else extract_text_from_word(uploaded_file2)
        else:
            text2 = st.text_area("Paste Text 2", height=200)

    if st.button("Check Similarity"):
        if text1.strip() and text2.strip():
            similarity = calculate_similarity(text1, text2)
            st.success(f"Similarity: {similarity:.2f}%")
        else:
            st.warning("Please provide text in both fields.")

elif st.session_state.active_page == "Info about Plagiarism Checker":
    st.markdown("<h1 style='text-align: center;'>Info about Plagiarism Checker</h1>", unsafe_allow_html=True)
    
    st.write("""
    The **Plagiarism Checker** in this system leverages Natural Language Processing (NLP) techniques to compare two pieces of text and determine their similarity. Here's a detailed explanation of how it works in the context of NLP:
    """)

    st.markdown("---")

    st.header("1. Text Input and Preprocessing")
    st.write("""
    The process begins with the user providing two pieces of text, either by uploading files (PDF or Word) or by directly pasting text into input fields. If files are uploaded, the system extracts the text from these files. This step ensures that the text is in a format suitable for comparison.
    """)
    st.subheader("Text Extraction")
    st.write("""
    - For PDFs, the system reads the text from each page.
    - For Word documents, it extracts text from paragraphs.
    """)
    st.subheader("Preprocessing")
    st.write("""
    While not explicitly implemented in the code, preprocessing is a common step in NLP. This could include:
    - **Tokenization**: Splitting the text into words or sentences.
    - **Normalization**: Converting text to lowercase, removing punctuation, and handling special characters.
    - **Stopword Removal**: Eliminating common words (e.g., "the," "is") that do not contribute much to the meaning.
    - **Stemming/Lemmatization**: Reducing words to their base or root form (e.g., "running" → "run").
    """)

    st.markdown("---")

    st.header("2. Text Comparison Using Sequence Matching")
    st.write("""
    The core of the plagiarism checker relies on the **SequenceMatcher** algorithm from Python's `difflib` library. This algorithm is used to compare the two texts and calculate their similarity. Here's how it works in NLP terms:
    """)
    st.subheader("Sequence Alignment")
    st.write("""
    The algorithm aligns the two texts to find the longest contiguous matching subsequences. It identifies sequences of words or characters that are identical or nearly identical in both texts.
    """)
    st.subheader("Similarity Ratio")
    st.write("""
    The algorithm calculates a similarity score based on the length of the matching subsequences relative to the total length of the texts. This score is expressed as a ratio between 0 and 1, where:
    - **1** indicates that the texts are identical.
    - **0** indicates that the texts are completely different.
    """)
    st.subheader("Percentage Calculation")
    st.write("""
    The ratio is multiplied by 100 to convert it into a percentage, which is easier for users to interpret.
    """)

    st.markdown("---")

    st.header("3. NLP Techniques in Plagiarism Detection")
    st.write("""
    While the current implementation uses a simple sequence-matching approach, plagiarism detection in NLP often involves more advanced techniques. Here are some key concepts:
    """)
    st.subheader("a. Exact Matching")
    st.write("""
    - The system detects verbatim copying of text, where words or phrases are identical in both texts.
    - This is what the `SequenceMatcher` algorithm excels at.
    """)
    st.subheader("b. Fuzzy Matching")
    st.write("""
    - The system can identify near-exact matches, where small changes (e.g., synonyms, rephrasing, or minor edits) are made to the original text.
    - This is useful for detecting paraphrased content.
    """)
    st.subheader("c. Semantic Similarity")
    st.write("""
    - Advanced NLP models (e.g., BERT, GPT) can analyze the meaning of the text rather than just the surface-level words.
    - These models can detect plagiarism even when the wording is significantly altered but the ideas remain the same.
    """)
    st.subheader("d. Contextual Analysis")
    st.write("""
    - NLP systems can consider the context in which words or phrases are used. For example, the same word might have different meanings in different contexts, and advanced models can account for this.
    """)

    st.markdown("---")

    st.header("4. Limitations of the Current Approach")
    st.write("""
    The current implementation has some limitations from an NLP perspective:
    - **Surface-Level Comparison**: It only compares the text at a surface level and does not understand the meaning or context.
    - **No Semantic Analysis**: It cannot detect paraphrased content or ideas expressed in different words.
    - **No Citation Detection**: It does not distinguish between plagiarized content and properly cited references.
    """)

    st.markdown("---")

    st.header("5. How NLP Enhances Plagiarism Detection")
    st.write("""
    To improve the plagiarism checker, advanced NLP techniques can be incorporated:
    - **Word Embeddings**: Represent words as vectors in a high-dimensional space to capture their meanings and relationships.
    - **Sentence Embeddings**: Represent entire sentences as vectors to compare their semantic similarity.
    - **Pre-trained Language Models**: Use models like BERT or GPT to analyze the text at a deeper level and detect paraphrasing or rephrasing.
    - **Topic Modeling**: Identify the main topics in the text and compare them to detect content overlap.
    """)

    st.markdown("---")

    st.header("6. Practical Applications")
    st.write("""
    The plagiarism checker can be used in various scenarios:
    - **Academic Integrity**: Students and educators can use it to ensure originality in essays, research papers, and assignments.
    - **Professional Writing**: Writers and editors can check for unintentional plagiarism in articles, reports, and other documents.
    - **Content Creation**: Bloggers and content creators can verify that their work is unique and not copied from other sources.
    """)

    st.markdown("---")

    st.header("7. Workflow in NLP Terms")
    st.write("""
    1. **Input**: Two pieces of text are provided by the user.
    2. **Preprocessing**: The text is cleaned and prepared for analysis (if advanced techniques are used).
    3. **Comparison**: The system compares the texts using sequence matching or advanced NLP models.
    4. **Similarity Calculation**: A similarity score is calculated based on the comparison.
    5. **Output**: The similarity percentage is displayed to the user.
    """)

    st.markdown("---")

    st.header("8. Future Improvements")
    st.write("""
    To make the plagiarism checker more robust, you could:
    - Integrate **semantic analysis** to detect paraphrased content.
    - Add **citation detection** to identify properly referenced material.
    - Use **machine learning models** to improve accuracy and handle larger datasets.
    """)

    st.markdown("---")

    st.write("""
    In summary, the plagiarism checker in this system uses basic NLP techniques (sequence matching) to compare two texts and calculate their similarity. While it is effective for detecting exact or near-exact matches, it can be enhanced with advanced NLP methods to handle more complex cases of plagiarism.
    """)

elif st.session_state.active_page == "Chatbot":
    st.markdown("<h1 style='text-align: center;'>Chatbot</h1>", unsafe_allow_html=True)

    # Display chat history with enhanced styling
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(
                f"<div style='background-color: #1A5276; color: white; padding: 10px; border-radius: 10px; "
                f"margin-bottom: 10px; font-size: 16px;'>"
                f"<strong>User:</strong> {message['content']}</div>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"<div style='background-color: #4A235A; color: white; padding: 10px; border-radius: 10px; "
                f"margin-bottom: 10px; font-size: 16px; border: 1px solid #6C3483;'>"
                f"<strong>Bot:</strong> {message['content']}</div>",
                unsafe_allow_html=True,
            )

    # Clear Chat Button
    if st.button("Clear Chat"):
        st.session_state.chat_history = []

    # Chat input at the bottom of the sidebar
    st.text_input(
        "Type your message and press Enter",
        key="user_input_buffer",
        on_change=submit_message,
        placeholder="Ask the chatbot...",
    )