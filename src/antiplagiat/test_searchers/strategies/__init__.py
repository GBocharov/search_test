import chromadb

local_client = chromadb.HttpClient(host="localhost", port=8000)
print(local_client.list_collections())
