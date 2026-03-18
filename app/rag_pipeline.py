import chromadb
from app.embeddings import model
from groq import Groq
from app.core.config import GROQ_API_KEY
from datetime import datetime

# Groq setup
groq_client = Groq(api_key=GROQ_API_KEY)

chroma_client = chromadb.Client()

collection = chroma_client.get_or_create_collection(
    name="website_knowledge"
)


def store_embeddings(chunks: list, embeddings):
    ids = [f"chunk_{i}_{int(datetime.now().timestamp())}" for i in range(len(chunks))]
    collection.add(
        documents=chunks,
        embeddings=[e.tolist() for e in embeddings],
        ids=ids
    )


def direct_answer(question: str) -> str:
    """Fallback: Groq se direct answer bina context ke"""
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": question}],
        max_tokens=1024
    )
    return response.choices[0].message.content


def rag_answer(question: str):
    try:
        q_embedding = model.encode([question])[0]

        results = collection.query(
            query_embeddings=[q_embedding.tolist()],
            n_results=3
        )

        docs = results.get("documents", [[]])[0]

        # Context nahi mila — fallback to direct answer
        if not docs:
            return direct_answer(question)

        context = "\n".join(docs)

        prompt = f"""You are a helpful assistant. Answer the question using the context provided below.
If the answer is not in the context, answer from your own knowledge.

Context:
{context}

Question: {question}"""

        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1024
        )

        answer = response.choices[0].message.content

        # Agar model ne bola "I don't have that information" — fallback
        fallback_phrases = ["i don't have that information", "not in the context", "no information"]
        if any(p in answer.lower() for p in fallback_phrases):
            return direct_answer(question)

        return answer

    except Exception as e:
        print(f"Error in rag_answer: {e}")
        return f"Error generating answer: {str(e)}"


def search_chunks(query: str):
    query_embedding = model.encode([query])
    results = collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results=3
    )
    return results
