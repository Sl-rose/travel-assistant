import chromadb
import os
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction


chroma_client = chromadb.PersistentClient(path="./chromadb")

collection = chroma_client.get_or_create_collection(
    name="collection_0424",
    embedding_function=OpenAIEmbeddingFunction(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        model_name="text-embedding-v4",
        api_base="https://dashscope.aliyuncs.com/compatible-mode/v1",
        api_type="dashscope",  
    )
)

if __name__ == "__main__":
    result=collection.query(query_texts=["赵春哲的电话"])
    print(result)