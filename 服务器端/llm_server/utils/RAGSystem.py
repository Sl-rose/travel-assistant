import chromadb
import os
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from sentence_transformers import CrossEncoder
#加载二次精排模型
from django.conf import settings
BASE_DIR = settings.BASE_DIR



class RAGSystem:
    def __init__(self):
        chroma_client = chromadb.PersistentClient(path="./chromadb")
        self.collection = chroma_client.get_or_create_collection(
            name="collection_0424",
            embedding_function=OpenAIEmbeddingFunction(
                api_key=os.getenv("DASHSCOPE_API_KEY"),
                model_name="text-embedding-v4",
                api_base="https://dashscope.aliyuncs.com/compatible-mode/v1",
                api_type="dashscope",  
            ),
        )

        # 加载二次精排模型
        model_path = os.path.join(BASE_DIR, "models")
        print("模型路径为：",model_path)
        self.model = CrossEncoder(model_path)
    def retrieval_chunks(self,question,rerank=True,rank_threshold=0.5):
        result=self.collection.query(query_texts=[question],n_results=5)
        # 只需要里面的documents部分
        documents = result["documents"][0]
        # 元消息
        metadatas = result["metadatas"][0]
        # 相似度
        distances = result["distances"][0]
        if rerank:
            ranks = self.model.rank(question,documents,return_documents=True)
            print("Query:",question)
            for rank in ranks:
                print(f"- #{rank['corpus_id'] } ({rank['score']:.2f}): {rank['text'][:50]}", flush=True)

        return {"documents":documents,"metadatas":metadatas,"distances":distances}

    