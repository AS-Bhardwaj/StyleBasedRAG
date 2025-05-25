import chromadb
from chromadb.config import Settings
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

class VectorDBService:
    def __init__(self, persistent_directory="chroma_db", embedding_function=None):
        self.client = chromadb.PersistentClient(path=persistent_directory)
        # You can plug in any embedding function here. OpenAI is used as an example.
        self.embedding_function = embedding_function
        # self.embedding_function = embedding_function or OpenAIEmbeddingFunction(
        #     api_key="your-openai-api-key",  # Replace this with your actual key or use os.getenv()
        #     model_name="text-embedding-3-small"
        # )
        self.collections = {}

    def create_collection(self, name):
        if name not in self.collections:
            self.collections[name] = self.client.create_collection(name=name, embedding_function=self.embedding_function)
        return self.collections[name]

    def get_collection(self, name):
        if name in self.collections:
            return self.collections[name]
        return self.client.get_collection(name=name, embedding_function=self.embedding_function)

    def delete_collection(self, name):
        if name in self.collections:
            del self.collections[name]
        self.client.delete_collection(name)

    def create_or_get_collection(self, name):
        try:
            # collection = self.client.get_or_create_collection(name=name)
            # return collection
            existing_collections = [col.name for col in self.client.list_collections()]
    
            if name in existing_collections:
                print(f"Collection '{name}' exists. Loading it.")
                return self.client.get_collection(name=name)
            else:
                print(f"Collection '{name}' not found. Creating it.")
                return self.client.create_collection(name=name)
        except Exception:
            print("RUNNING EXCEPTION")
            return self.create_collection(name)

    def add_document(self, collection_name, documents, metadatas=None, ids=None):
        collection = self.create_or_get_collection(collection_name)
        collection.add(
            documents=documents,
            metadatas=metadatas or [{} for _ in documents],
            ids=ids or [f"doc_{i}" for i in range(len(documents))]
        )

    def get_similar_document(self, collection_name, query_text, top_k=3):
        collection = self.get_collection(collection_name)
        return collection.query(query_texts=[query_text], n_results=top_k)

    def delete_document(self, collection_name, ids):
        collection = self.get_collection(collection_name)
        collection.delete(ids=ids)
