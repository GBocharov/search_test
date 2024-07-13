from text_utils.text_cleaners.cleaning_finctions import SimpleCleanFunction
from text_utils.text_splitters.ru_token_splitter import RU_TOKEN_SPLITTER


from data_processing.embedding_functions import LocalAllMiniEmbeddingFunctionCleaned
from data_processing.output_parse_functions import SimpleOutputParser
from vector_storage.infrastructure.chroma_db_config import chroma_db_config

from data_processing.parse_inserts_functions import SimpleIdeasInsertParser
from data_processing.parse_request_functions import SimpleIdeasRequestsParser
from vector_storage.domain.Strategy import Strategy

text_cleaning_f = SimpleCleanFunction()
text_splitter = RU_TOKEN_SPLITTER(tokens_per_chunk=500, chunk_overlap=50)

inserts_parse_f = SimpleIdeasInsertParser(text_splitter)
request_parse_f = SimpleIdeasRequestsParser(text_splitter)
output_parse_f = SimpleOutputParser()

model_path = '/opt/app-root/models/paraphrase-multilingual-MiniLM-L12-v2'
embedding_f = LocalAllMiniEmbeddingFunctionCleaned(model_path, text_cleaning_f)

collection_name = 'Mini_12_cleaner_collection'

#chroma_client = chromadb.HttpClient(host=chroma_db_config.HOST, port=chroma_db_config.PORT)

strategy = Strategy(
    collection_name=collection_name,
    parse_inserts_f=inserts_parse_f,
    parse_output_f=output_parse_f,
    parse_search_requests_f=request_parse_f,
    embedding_f=embedding_f
)

