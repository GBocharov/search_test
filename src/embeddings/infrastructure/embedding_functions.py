from chromadb import EmbeddingFunction, Documents, Embeddings
from sentence_transformers import SentenceTransformer


# async?
class LocalAllMiniEmbeddingFunction(EmbeddingFunction[Documents]):
    def __init__(self, model_path: str):
        self.embeddings = SentenceTransformer(model_path)

    def __call__(self, input: Documents) -> Embeddings:
        e = self.embeddings.encode(input, normalize_embeddings=True).tolist()
        return e

model_path = '/opt/app-root/models/paraphrase-multilingual-MiniLM-L12-v2'
local_embedding_function = LocalAllMiniEmbeddingFunction(model_path)
