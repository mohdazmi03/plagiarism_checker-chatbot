# plagiarism_checker-chatbot
A web app built with Streamlit that offers two main features: plagiarism checking (comparing text files or pasted content) and a chatbot powered by Ollama Gemma2:2b. Users can upload PDF/Word files for plagiarism detection and interact with the chatbot for NLP-related queries.
Plagiarism Checker & Chatbot Application
This application combines two functionalities: a Plagiarism Checker and a Chatbot. The Plagiarism Checker allows users to compare two pieces of text (from PDF or Word files or pasted text) and calculate their similarity. The Chatbot provides educational responses about plagiarism and plagiarism detection using Natural Language Processing (NLP) techniques.

**Features**
1. Plagiarism Checker
Upload PDF or Word Files: Users can upload two files for plagiarism checking.
Text Comparison: The system extracts text from the uploaded files, compares them, and calculates their similarity using the difflib library.
Similarity Calculation: The similarity score is displayed as a percentage.
2. Chatbot
Interactive Chat: Users can chat with the bot, which is designed to answer queries related to plagiarism and plagiarism checking.
Conversation History: The chatbot remembers the conversation history, providing context for better responses.
Guided Responses: The chatbot uses a pre-defined prompt and Ollama’s Gemma2:2b model to generate accurate, helpful responses.
3. Info about Plagiarism Checker
NLP Explanation: Provides detailed information about how the plagiarism checker works, explaining text extraction, similarity calculation, and NLP techniques like fuzzy matching and semantic similarity.

****How to Use****
**Plagiarism Checker:**
Upload Two Files: You can upload two files (PDF or Word) to check their similarity.
Text Input: Alternatively, you can paste text into the provided text areas for comparison.
Similarity Result: After uploading both files or pasting text, click the Check Similarity button to see the percentage of similarity between the two texts.

**Chatbot:**
Start Chatting: Enter your question about plagiarism or plagiarism checking in the input box.
Chat History: The chatbot keeps a history of your messages to maintain context and provide more accurate answers.
Clear Chat: You can clear the chat history by clicking the Clear Chat button.

**Info about Plagiarism Checker:**
Learn about how the plagiarism checker works, including the NLP techniques used for text comparison and the limitations of the current approach.

**Technologies Used**
Streamlit: For building the web interface.
Ollama Gemma2:2b model: For generating chatbot responses.
difflib (SequenceMatcher): For comparing two pieces of text.
PyPDF2: For extracting text from PDF files.
python-docx: For extracting text from Word documents.

**Contributing**
Contributions are welcome! If you find any bugs or have suggestions for improvements, feel free to open an issue or submit a pull request.

**License**
This project is open-source and available under the MIT License.
