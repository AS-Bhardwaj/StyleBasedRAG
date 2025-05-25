import gradio as gr
from main import RAGMain
from all_character_style_summary import all_characters_style_summary_dict

# Initialize the RAG agent once
prompt = f"""
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
    system_prompt=prompt
)

# Prepare vector DB only if needed
rag_agent.prepare_documents()

# Available characters
CHARACTER_OPTIONS = list(all_characters_style_summary_dict.keys())

# Chat function
def chat_with_character(user_message, selected_character, chat_history:list=[]):
    print(selected_character)
    character_style_summary = all_characters_style_summary_dict[selected_character]
    result = rag_agent.get_response(user_message, character_style_summary)
    bot_response = result["response"]
    chat_history.append({"role": "user", "content": user_message})
    chat_history.append({"role": "assistant", "content": bot_response})
    return chat_history, chat_history

# Gradio UI
with gr.Blocks(title="🧙‍♂️ Chat with Harry Potter Characters") as demo:
    gr.Markdown("# 🧙 Chat with a Character from *Harry Potter and the Sorcerer's Stone*")
    with gr.Row():
        character_selector = gr.Dropdown(choices=CHARACTER_OPTIONS, label="Choose a Character", value=CHARACTER_OPTIONS[0])
    
    chatbot = gr.Chatbot(label="Magical Dialogue", height=400, type="messages")
    user_input = gr.Textbox(label="Your Message", placeholder="Ask something magical...")
    state = gr.State([])

    send_button = gr.Button("Send")

    send_button.click(
        fn=chat_with_character,
        inputs=[user_input, character_selector, state],
        outputs=[chatbot, state]
    )

    user_input.submit(
        fn=chat_with_character,
        inputs=[user_input, character_selector, state],
        outputs=[chatbot, state]
    )

# Run
if __name__ == "__main__":
    demo.launch()
