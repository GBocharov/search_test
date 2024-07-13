from chromadb import EmbeddingFunction, Documents, Embeddings
from sentence_transformers import SentenceTransformer

from text_utils.text_cleaners.cleaning_finctions import CleaningFunction, text_cleaning_f


# async?
class LocalAllMiniEmbeddingFunction(EmbeddingFunction[Documents]):
    def __init__(self, model_path: str):
        self.embeddings = SentenceTransformer(model_path)

    def __call__(self, input: Documents) -> Embeddings:
        e = self.embeddings.encode(input, normalize_embeddings=True).tolist()
        return e


class LocalAllMiniEmbeddingFunctionCleaned(EmbeddingFunction[Documents]):
    def __init__(self, model_path: str, clean_f: CleaningFunction):
        self.embeddings = SentenceTransformer(model_path)
        self.clean_f = clean_f

    def __call__(self, inputs: Documents) -> Embeddings:
        cleaned_inputs = self.clean_f(inputs)
        e = self.embeddings.encode(cleaned_inputs, normalize_embeddings=True).tolist()
        return e



model_path = '/opt/app-root/models/paraphrase-multilingual-MiniLM-L12-v2'
local_embedding_function = LocalAllMiniEmbeddingFunctionCleaned(model_path, text_cleaning_f)

