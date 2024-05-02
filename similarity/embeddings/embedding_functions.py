from chromadb import Documents, EmbeddingFunction, Embeddings
from chromadb.utils import embedding_functions
# from sentence_transformers import SentenceTransformer


class MyEmbeddingFunction(EmbeddingFunction):
    def __call__(self, input: Documents) -> Embeddings:
        
        embeddings: list[list[int]] = [[]]
        # Define custom embeddings here

        return embeddings



def chroma_embeddings():
    return print(type(embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")))
    # return embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")


chroma_embeddings()