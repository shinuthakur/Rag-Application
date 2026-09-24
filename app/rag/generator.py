from langchain_core.documents import Document
from langchain_google_genai import ChatGoogleGenerativeAI

from app.config import settings


class RAGGenerator:
    SYSTEM_PROMPT = """
You are a retrieval-augmented generation assistant.

Your job is to answer the user's question using ONLY
the information provided in the retrieved context.

Rules:
1. Do not use outside knowledge.
2. Do not make up or infer facts that are not supported
   by the context.
3. If the answer cannot be found in the context, clearly say:
   "I could not find the answer in the provided source."
4. Give a direct and useful answer.
5. Preserve important technical terms from the source.
6. When useful, organize the answer with short paragraphs
   or bullet points.
"""

    def __init__(self):
        if not settings.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY is not configured.")

        self.primary_llm = ChatGoogleGenerativeAI(
            model=settings.LLM_MODEL,
            google_api_key=settings.GOOGLE_API_KEY,
            max_retries=2,
        )

        self.fallback_llm = ChatGoogleGenerativeAI(
            model=settings.LLM_FALLBACK_MODEL,
            google_api_key=settings.GOOGLE_API_KEY,
            max_retries=2,
        )

    def generate(
        self,
        question: str,
        documents: list[Document],
    ) -> str:

        if not question.strip():
            raise ValueError("Question cannot be empty.")

        if not documents:
            return "I could not find the answer in the provided source."

        context_parts = []

        for index, document in enumerate(documents, start=1):
            context_parts.append(
                f"[Context {index}]\n{document.page_content}"
            )

        context = "\n\n".join(context_parts)

        prompt = f"""
{self.SYSTEM_PROMPT}

Retrieved Context:
------------------
{context}
------------------

User Question:
{question}

Answer:
"""

        try:
            response = self.primary_llm.invoke(prompt)

        except Exception as exc:
            error_text = str(exc).upper()

            if "503" not in error_text and "UNAVAILABLE" not in error_text:
                raise

            response = self.fallback_llm.invoke(prompt)

        if isinstance(response.content, str):
            return response.content.strip()

        return str(response.content).strip()