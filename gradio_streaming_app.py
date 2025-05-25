import gradio as gr
from main import RAGMain
from all_character_style_summary import all_characters_style_summary_dict

# ─── 1. Initialize RAG agent and index documents ──────────────────────────────
SYSTEM_PROMPT = f"""
You are an AI agent trained to impersonate characters from *Harry Potter and the Sorcerer's Stone*. 

Your task is to:
1. Identify which character the question is about OR which character is expected to answer.
2. Respond in that character's unique voice, tone, and personality.
3. Use only the factual information provided in the context below — do not make up facts.

## Character Style Guide
character_style_summary

## Context (retrieved from book)
kb_context

## Output Instructions
- Respond exactly as the identified character would — based on their personality and behavior.
- Use natural dialogue and language consistent with how that character speaks.
- Ground your answer in the retrieved context and known traits of the character.

Respond below:
"""

rag_agent = RAGMain(
    kb_text_path="harryporter_1.txt",
    system_prompt=SYSTEM_PROMPT
)
rag_agent.prepare_documents()

CHARACTER_OPTIONS = list(all_characters_style_summary_dict.keys())

# ─── 2. Non-streaming chat function (fallback) ─────────────────────────────────
def chat_with_character(user_message, selected_character, chat_history):
    style = all_characters_style_summary_dict[selected_character]
    result = rag_agent.get_response(user_message, style)
    bot_text = result["response"]

    chat_history.append({"role": "user",      "content": user_message})
    chat_history.append({"role": "assistant", "content": bot_text})
    return chat_history, chat_history

def stream_with_character(user_message, selected_character, chat_history):
    style = all_characters_style_summary_dict[selected_character]
    yield from rag_agent.stream_response_gradio(user_message, style, chat_history)

with gr.Blocks() as demo:
    gr.Markdown("# 🧙 Chat with Harry Potter Characters")
    selector = gr.Dropdown(CHARACTER_OPTIONS, label="Character")
    chatbot = gr.Chatbot(type="messages", label="Chat")
    user_input = gr.Textbox(placeholder="Your question…")
    state = gr.State([])

    user_input.submit(
        fn=stream_with_character,
        inputs=[user_input, selector, state],
        outputs=[chatbot, state]
    )

if __name__ == "__main__":
    demo.launch()
