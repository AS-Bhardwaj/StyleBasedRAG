import os
from typing import List, Dict
from textconverter import TextConverter  # You should implement this
from retriever import VectorDBService
from generator import LLM
from chunker import TextSplitter
from all_character_style_summary import all_characters_style_summary_dict


class RAGMain:
    def __init__(self, kb_pdf_path: str=None,
                 kb_text_path:str=None, 
                 collection_name: str = "harry_potter", 
                 persist_directory:str="./chromadb/", 
                 openai_llm_model:str='gpt-4.1-mini',
                 temperature:int=0.5,
                 chunk_size:int=1000,
                 chunk_overlap:int=200, 
                 conv_history:list=[],
                 system_prompt:str="You are a helpful assistant",
                 conversation_history_length:int=6,
                 ):
        self.kb_pdf_path = kb_pdf_path
        self.kb_text_path = kb_text_path
        self.collection_name = collection_name
        self.persistant_directory = persist_directory + collection_name
        self.vector_db = VectorDBService(persistent_directory=self.persistant_directory)
        
        self.system_prmpt = system_prompt
        self.conv_history = [{"role":"system","content":system_prompt}] if len(conv_history)==0 else conv_history
        
        self.llm = LLM(model=openai_llm_model, temperature=temperature, conversation_history_length=conversation_history_length)
        self.splitter = TextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    def prepare_documents(self, output_text_file_path:str=None):
        """Load PDF, split text, and add to vector database."""
        print("[INFO] Loading and splitting PDF...")
        
        if self.kb_text_path!=None:
            raw_text = TextConverter.read_from_text_file(self.kb_text_path)
        elif self.kb_text_path==None and self.kb_pdf_path!=None:
            loader = TextConverter.pdf_to_text(self.kb_pdf_path, output_text_file_path=output_text_file_path)
            raw_text = loader.extract_text()
        else:
            raw_txt=''
            print("No KB Provided. Both kb_pdf_path and kb_text_path can't be empt, provide one.")
        
        if raw_text!=None:
            chunks = self.splitter.split_by_length(raw_text)
            docs = [{"id": f"doc_{i}", "content": chunk, "metadata": {"source": f"page_{i}"}} for i, chunk in enumerate(chunks)]
            docs_content=[i["content"] for i in docs]
            docs_metadata = [i["metadata"] for i in docs]
            docs_id = [i["id"] for i in docs]
            print("[INFO] Storing chunks in ChromaDB...")
            # self.vector_db.create_or_get_collection(self.collection_name)
            self.vector_db.add_document(self.collection_name, documents=docs_content, metadatas=docs_metadata, ids=docs_id)
        else:
            print("No Vector DB is Created as there was no KB provided.")
            
    def get_response(self, user_query: str, character_style_summary:str=None) -> Dict:
        """Handles user query and returns LLM response."""
        # print(f"[INFO] Query: {user_query} | Character: {character}")

        result = self.vector_db.get_similar_document(
            collection_name=self.collection_name,
            query_text=user_query,
            top_k=5
        )
        relevant_chunks = result["documents"][0]
        # print(relevant_chunks)
        context = "\n\n".join(relevant_chunks)

        self.conv_history[0]['content'] = self.conv_history[0]['content'].replace("kb_context",str(context)).replace("character_style_summary",str(character_style_summary))
        
        self.conv_history.append({"role":"user", "content":user_query})
        
        response = self.llm.get_response(self.system_prmpt, conv_history=self.conv_history)
        
        self.conv_history.append({"role":"assistant", "content":response})
        
        self.conv_history[0]['content'] = self.conv_history[0]['content'].replace(str(context), "kb_context").replace(str(character_style_summary),"character_style_summary")

        return {
            "response": response,
            "retrieved_chunks": relevant_chunks
        }
    def stream_response_gradio(self, user_message: str, character_style_summary: str, chat_history: List[Dict]):
        """
        Gradio generator: yields (chat_history, chat_history) on every delta.
        """
        # 1) Retrieve and build context
        result = self.vector_db.get_similar_document(
            collection_name=self.collection_name,
            query_text=user_message,
            top_k=5
        )
        chunks = result["documents"][0]
        context = "\n\n".join(chunks)

        # 2) Build system prompt with injected context & style
        self.conv_history[0]['content'] = self.conv_history[0]['content'].replace("kb_context", str(context))\
                                  .replace("character_style_summary", str(character_style_summary))

        # 3) Update history: user + empty assistant
        chat_history.append({"role": "user",      "content": user_message})
        chat_history.append({"role": "assistant", "content": ""})

        # 4) Stream deltas into the last assistant message
        #    Pass a fresh conv_history to LLM
        self.conv_history.append({"role":"user","content":user_message})
        for delta in self.llm.get_streaming_response(conv_history=self.conv_history):
            chat_history[-1]["content"] += delta
            yield chat_history, chat_history

        # 5) Finalize internal history
        full_response = chat_history[-1]["content"]
        self.conv_history.append({"role":"assistant", "content": full_response})
        self.conv_history[0]['content'] = self.conv_history[0]['content'].replace(str(context), "kb_context").replace(str(character_style_summary),"character_style_summary")

if __name__ == "__main__":
    # rag_agent = RAGMain(pdf_path="Harry_Potter_and_the_Sorcerers_Stone.pdf")
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
    rag_agent = RAGMain(kb_text_path="harryporter_1.txt", system_prompt=prompt)
    # Only run once or when collection needs update
    rag_agent.prepare_documents()
    while True:
        user_query = input('Enter your query.... : ')
        character = input('Which Character : ')
        character_style_summary = all_characters_style_summary_dict[character]
        print("USER : ", user_query)
        result = rag_agent.get_response(
            # user_query="What would you do if you found a mysterious artifact in Hogwarts?",
            user_query=user_query,
            character_style_summary=character_style_summary
        )

        print("=== Response ===")
        print("AI : ",result["response"])
        # print("\n=== Explanation (Chunks) ===")
        # for chunk in result["retrieved_chunks"]:
        #     print("-", chunk[:150], "...")
