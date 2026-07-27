"""
Practice RAG — Inventory & Sales Policy Assistant (with persistence)
Stack: Groq (LLM) + Jina (embeddings) + FAISS (vector store) + LangChain
"""
import config
config.check_api_keys()  # fail fast, before touching any data or APIs

from ingestion import get_vector_store
from langchain_groq import ChatGroq
from langchain.agents import create_agent

vector_store = get_vector_store()  # builds once, loads instantly every run after
retriever = vector_store.as_retriever(search_kwargs={"k": config.RETRIEVAL_TOP_K})


def search_policy(question: str) -> str:
    """Search Inventory & Sales policies for returns, discounts, terms."""
    chunks = retriever.invoke(question)
    return "\n\n".join(c.page_content for c in chunks)


llm = ChatGroq(model=config.LLM_MODEL_NAME, temperature=0)
assistant = create_agent(model=llm, tools=[search_policy], system_prompt=config.SYSTEM_PROMPT)


def ask_assistant(question: str) -> str:
    print("=" * 60)
    print("Q:", question)
    print("-" * 60)
    response = assistant.invoke({"messages": [{"role": "user", "content": question}]})
    answer = response["messages"][-1].content
    print("A:", answer)
    return answer


if __name__ == "__main__":
    # The vector store, retriever and agent above are built once, before this
    # loop starts — so every question reuses them instead of re-embedding.
    print("Ask a question (blank line to quit).")
    while True:
        question = input("\n> ").strip()
        if not question:
            break
        ask_assistant(question)
