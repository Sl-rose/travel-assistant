import chromadb
import os
import json
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
# md5
import hashlib

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
    # 原始文档块路径
    chunks_path = "./chunks/knowledges.json"
    # 读取里面的json格式数据
    with open(chunks_path, "r", encoding="utf-8") as f:
        chunks = json.load(f)
        print(chunks)
        ids,documents,metadatas = [],[],[]
        for chunk in chunks:
            ids.append(
                hashlib.md5(
                    (chunk["content"]+str(chunk["metadata"])).encode("utf-8")
                ).hexdigest()
            )
            documents.append(chunk["content"])
            metadatas.append(chunk["metadata"])
    
    batch_size = 10
    total_chunks = len(ids)

    for i in range(0, total_chunks, batch_size):
        end_idx = min(i+batch_size,total_chunks)
        batch_ids = ids[i:end_idx]
        batch_documents = documents[i:end_idx]
        batch_metadatas = metadatas[i:end_idx]

        print(f"正在添加{i+1}-{end_idx}条记录，共{total_chunks}条")

            
        collection.add(
            #不能重复的ID
            ids=batch_ids,  
            #文档内容
            documents=batch_documents,  
            #元数据：具备可解释性
            metadatas=batch_metadatas,
)
#总共多少条记录
print(f"\n添加完成！总共{collection.count()}条记录")
# 显示前面5条记录
print("\n前5条记录预览：")
print(collection.peek(5))