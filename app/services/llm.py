import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

client = InferenceClient(api_key=HF_TOKEN)

class AnswerService:
    def generate_answer(self, question: str, context: str) -> str:
        prompt = f"""
            You are a helpful assistant. Use the context below to answer the user's question.

            Context:
            {context}

            Question: {question}
            Answer:
            """
        try:
            response = client.chat.completions.create(
                model="mistralai/Mistral-7B-Instruct-v0.2",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300,
                temperature=0.7,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error generating answer: {str(e)}"
