Here’s a detailed and professional `README.md` for your **Style-Based RAG Chatbot** project:

---

```markdown
# 🧙‍♂️ Harry Potter Character Chatbot (Style-Based RAG)

This is an AI-powered chatbot that impersonates characters from *Harry Potter and the Sorcerer's Stone*, powered by Retrieval-Augmented Generation (RAG) and style conditioning. You can chat with characters like Harry, Hermione, Dumbledore, and more — and each response reflects their unique voice and personality.

---

## 🔮 Features

- 🎭 **Style-Based Response Generation**: Each character has a unique speaking style.
- 📚 **RAG Integration**: Context is retrieved from the actual book to ground answers.
- 📜 **No Hallucination**: All responses are based strictly on the content of the book.
- ⏱️ **Streaming Support**: Responses stream live via Gradio interface.
- ✅ **Character Selector**: Choose your favorite character to converse with.

---

## 🏗️ Project Structure

```

.
├── src/
│   ├── main.py                     # Core RAG logic
│   ├── generator.py                # Handles LLM interaction and streaming
│   ├── gradio\_streaming\_app.py     # Gradio frontend integration
│   └── ...
├── data/
│   └── harryporter\_1.txt           # Knowledge base (book text)
├── all\_character\_style\_summary.py  # Character voice/personality guide
├── requirements.txt
└── README.md

````

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/AS-Bhardwaj/StyleBasedRAG.git
cd StyleBasedRAG
````

### 2. Create and Activate a Virtual Environment

```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the App

```bash
python src/gradio_streaming_app.py
```

The app will be available at: [http://127.0.0.1:7860](http://127.0.0.1:7860)

---

## 🧠 How It Works

1. **User Input**: You ask a question.
2. **Character Style Conditioning**: The system loads that character’s style guide.
3. **Context Retrieval**: Relevant book passages are retrieved using vector search.
4. **Prompt Construction**: A prompt is dynamically built with the character style + context.
5. **LLM Streaming**: A large language model (e.g., GPT) responds in the chosen style.
6. **Streaming to UI**: The response is streamed live in the Gradio interface.

---

## 👥 Supported Characters

* Harry Potter
* Hermione Granger
* Ron Weasley
* Dumbledore
* Hagrid
* Draco Malfoy
* ... and more!

Each character is defined in `all_character_style_summary.py`.
For more characters, you can add their character style summary in all_character_style_summary.py like this "Harry Potter": 
    ```bash
    {
        "name": "Harry Potter",
        "style_tone": "Curious, brave, humble, often unsure but determined.",
        "summary": "An orphan raised by unkind relatives, Harry is discovering a magical world where he is famous. He is loyal, courageous, and always seeks the truth even when it scares him."
    }
    ```
```
