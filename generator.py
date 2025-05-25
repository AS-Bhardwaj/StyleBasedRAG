import os
from openai import OpenAI
from typing import List, Optional, Union

class LLM:
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o", temperature: float = 0.7,conversation_history_length:int=6):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY is not set in environment or provided directly.")

        self.client = OpenAI(api_key=self.api_key)
        self.model = model
        self.temperature = temperature
        self.conversation_history_length=conversation_history_length

    def get_response(
        self,
        user_query: str,
        conv_history: Optional[List[dict]] = None,
        system_prompt: str = "You are a helpful assistant.",
        max_tokens: int = 1024
    ) -> str:
        # messages = [{"role": "system", "content": system_prompt}]
        # if conv_history:
        #     messages.extend(conv_history)
        # messages.append({"role": "user", "content": user_query})

        try:
            print("Messages are : ", [conv_history[0]]+conv_history[1:][-self.conversation_history_length+1:])
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[conv_history[0]]+conv_history[1:][-self.conversation_history_length+1:],
                temperature=self.temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"[ERROR] Failed to get response: {e}"

    def get_streaming_response(self, conv_history: List[dict]):
        """
        Yields text deltas as strings from the OpenAI streaming API.
        """
        history = [conv_history[0]] + conv_history[1:][-self.conversation_history_length + 1:]
        stream = self.client.chat.completions.create(
            model=self.model,
            messages=history,
            temperature=self.temperature,
            stream=True
        )

        for chunk in stream:
            # each chunk.choices[0].delta is a ChoiceDelta with .content
            delta = getattr(chunk.choices[0].delta, "content", None)
            if delta:
                yield delta

    def summarize_text(self, text: str, summary_prompt: str = "Summarize this text:") -> str:
        return self.get_response(f"{summary_prompt}\n\n{text}")

    def analyze_character_traits(self, text: str, character_name: str) -> str:
        return self.get_response(
            f"Analyze the personality, tone, speaking style, and behavior of the character '{character_name}' based on this text:\n\n{text}",
            system_prompt="You are a literary character analyst and expert."
        )
