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


def rag_answer(question: str):
    try:
        q_embedding = model.encode([question])[0]

        results = collection.query(
            query_embeddings=[q_embedding.tolist()],
            n_results=3
        )

        docs = results.get("documents", [[]])[0]

        if not docs:
            return None

        context = "\n".join(docs)

        prompt = f"""You are a helpful assistant. Answer the question using ONLY the context provided below. 
If the answer is not in the context, say 'I don't have that information.'

Context:
{context}

Question: {question}"""

        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1024
        )

        return response.choices[0].message.content

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