import os
import sys

# 如果当前目录下存在 `chromadb/` 文件夹（例如存放 sqlite），会遮蔽 pip 安装的 chromadb 包。
# 这里移除 cwd 路径，确保导入到的是正确的 chromadb。
cwd = os.getcwd()
if os.path.isdir(os.path.join(cwd, "chromadb")):
    sys.path = [p for p in sys.path if p not in ("", cwd)]

import chromadb  # noqa: E402

if __name__ == "__main__":
    # 删除整个 collection（等价于删掉其中全部向量/文档）
    # 注意：删除后如果你再 get_or_create_collection，会重新创建一个空的 collection
    chroma_client = chromadb.PersistentClient(path="./chromadb")
    chroma_client.delete_collection(name="collection_0424")
    print("已删除 collection_0424")