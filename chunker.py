from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List

class TextSplitter:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split_by_length(self, text: str) -> List[str]:
        """Splits text using recursive character splitter based on chunk size and overlap."""
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n\n", "\n", ".", " ", ""]
        )
        return splitter.split_text(text)

    def split_by_special_string(self, text: str, special_string: str) -> List[str]:
        """Splits text using a custom delimiter."""
        return [chunk.strip() for chunk in text.split(special_string) if chunk.strip()]

    def split_by_paragraphs(self, text: str) -> List[str]:
        """Splits text by paragraph blocks."""
        return self.split_by_special_string(text, "\n\n")

    def split_by_sentences(self, text: str) -> List[str]:
        """Basic sentence splitter (does not use NLP)."""
        import re
        return [sentence.strip() for sentence in re.split(r'(?<=[.!?]) +', text) if sentence.strip()]
    
    