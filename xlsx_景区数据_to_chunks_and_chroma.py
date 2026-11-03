import argparse
import hashlib
import json
import os
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd


def _safe_str(v: Any) -> str:
    if v is None:
        return ""
    if isinstance(v, float) and pd.isna(v):
        return ""
    if isinstance(v, str):
        return v.strip()
    return str(v).strip()


def _get_col(df: "pd.DataFrame", idx: int, fallback: str) -> str:
    try:
        return str(df.columns[idx])
    except Exception:
        return fallback


def _row_to_chunk(
    row: "pd.Series",
    source_name: str,
    row_index_1based: int,
    colnames: List[str],
) -> Optional[Dict[str, Any]]:
    # 该样本文件常见列（按你文件读取到的列顺序）：
    # 0: 景区等级  1: 省份  2: 景区名称  3: 经纬度  4: 景区地址
    # 5: 简介      6: 标签  7: 票价      8: 开放时间
    # 9: 最佳季节 10: 建议游玩时长 11+: 各类评级/名录（可能为空）
    level = _safe_str(row.iloc[0]) if len(row) > 0 else ""
    province = _safe_str(row.iloc[1]) if len(row) > 1 else ""
    name = _safe_str(row.iloc[2]) if len(row) > 2 else ""
    latlng = _safe_str(row.iloc[3]) if len(row) > 3 else ""
    address = _safe_str(row.iloc[4]) if len(row) > 4 else ""
    intro = _safe_str(row.iloc[5]) if len(row) > 5 else ""
    tags = _safe_str(row.iloc[6]) if len(row) > 6 else ""
    ticket = _safe_str(row.iloc[7]) if len(row) > 7 else ""
    open_time = _safe_str(row.iloc[8]) if len(row) > 8 else ""
    best_season = _safe_str(row.iloc[9]) if len(row) > 9 else ""
    suggested_time = _safe_str(row.iloc[10]) if len(row) > 10 else ""

    if not any([name, intro, address, tags]):
        return None

    extra_fields: List[Tuple[str, str]] = []
    for i in range(11, min(len(row), len(colnames))):
        v = _safe_str(row.iloc[i])
        if v:
            extra_fields.append((colnames[i], v))

    content_lines = [
        "【景区信息】",
        f"景区名称：{name}" if name else "",
        f"景区等级：{level}" if level else "",
        f"省份：{province}" if province else "",
        f"经纬度：{latlng}" if latlng else "",
        f"地址：{address}" if address else "",
        f"开放时间：{open_time}" if open_time else "",
        f"票价：{ticket}" if ticket else "",
        f"最佳季节：{best_season}" if best_season else "",
        f"建议游玩时长：{suggested_time}" if suggested_time else "",
        f"关键词：{tags}" if tags else "",
        f"简介：{intro}" if intro else "",
    ]
    for k, v in extra_fields:
        content_lines.append(f"{k}：{v}")

    content = "\n".join([x for x in content_lines if x]).strip()
    if not content:
        return None

    metadata: Dict[str, Any] = {
        "source": source_name,
        "row": row_index_1based,
        "type": "scenic_spot",
    }
    if name:
        metadata["name"] = name
    if province:
        metadata["province"] = province
    if level:
        metadata["level"] = level

    return {"metadata": metadata, "content": content}


def build_chunks_from_xlsx(xlsx_path: str, limit: int = 0) -> List[Dict[str, Any]]:
    df = pd.read_excel(xlsx_path)

    # 某些环境下列名/内容在控制台显示会乱码；写入 JSON 时会按字符串原样保存。
    colnames = [
        _get_col(df, i, f"col_{i}")
        for i in range(len(df.columns))
    ]

    source_name = os.path.basename(xlsx_path)
    chunks: List[Dict[str, Any]] = []
    n = len(df) if limit <= 0 else min(len(df), limit)
    for i in range(n):
        row = df.iloc[i]
        chunk = _row_to_chunk(row, source_name=source_name, row_index_1based=i + 1, colnames=colnames)
        if chunk:
            chunks.append(chunk)
    return chunks


def load_existing_chunks(json_path: str) -> List[Dict[str, Any]]:
    if not os.path.exists(json_path):
        return []
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            raw = f.read()
        if not raw.strip():
            return []
        data = json.loads(raw)
        return data if isinstance(data, list) else []
    except json.JSONDecodeError:
        # 现有文件为空/损坏时，按“没有现有 chunks”处理，避免整条流程被卡死
        return []


def dedupe_chunks(chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    seen = set()
    out: List[Dict[str, Any]] = []
    for c in chunks:
        content = _safe_str(c.get("content"))
        metadata = c.get("metadata", {})
        key = hashlib.md5((content + str(metadata)).encode("utf-8")).hexdigest()
        if key in seen:
            continue
        seen.add(key)
        out.append(c)
    return out


def save_chunks(json_path: str, chunks: List[Dict[str, Any]]) -> None:
    os.makedirs(os.path.dirname(json_path), exist_ok=True)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=4)


def add_chunks_to_chroma(
    chunks: List[Dict[str, Any]],
    host: str,
    port: int,
    collection_name: str,
) -> None:
    # 注意：你的项目根目录下有一个 `chromadb/` 文件夹（里面是 sqlite 文件），
    # 这会让 Python 优先把它当成名为 `chromadb` 的命名空间包，从而导致
    # `chromadb.utils...` 等 pip 包内容“消失”。
    #
    # 这里做一次防御性处理：如果 cwd 下存在 `chromadb/` 目录，则临时把 cwd 从 sys.path 移走，
    # 确保导入的是 pip 安装的 `chromadb`。
    import sys
    cwd = os.getcwd()
    if os.path.isdir(os.path.join(cwd, "chromadb")):
        sys.path = [p for p in sys.path if p not in ("", cwd)]

    import chromadb  # type: ignore

    try:
        from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction  # type: ignore
    except Exception as e:  # pragma: no cover
        raise RuntimeError(
            "无法导入 `OpenAIEmbeddingFunction`。通常是因为导入到了项目里的 `chromadb/` 目录而不是 pip 包，"
            "或当前 Python 环境未安装正确的 chromadb 依赖。"
        ) from e

    chroma_client = chromadb.HttpClient(host=host, port=port)
    collection = chroma_client.get_or_create_collection(
        name=collection_name,
        embedding_function=OpenAIEmbeddingFunction(
            api_key=os.getenv("DASHSCOPE_API_KEY"),
            model_name="text-embedding-v4",
            api_base="https://dashscope.aliyuncs.com/compatible-mode/v1",
            api_type="dashscope",
        ),
    )

    ids: List[str] = []
    documents: List[str] = []
    metadatas: List[Dict[str, Any]] = []
    for c in chunks:
        content = _safe_str(c.get("content"))
        metadata = c.get("metadata", {}) or {}
        ids.append(hashlib.md5((content + str(metadata)).encode("utf-8")).hexdigest())
        documents.append(content)
        metadatas.append(metadata)

    batch_size = 50
    for i in range(0, len(ids), batch_size):
        j = min(i + batch_size, len(ids))
        batch_ids = ids[i:j]
        batch_docs = documents[i:j]
        batch_metas = metadatas[i:j]

        # 兼容不同 chromadb 版本：优先 upsert，其次 add（add 可能因重复 id 报错）
        if hasattr(collection, "upsert"):
            collection.upsert(ids=batch_ids, documents=batch_docs, metadatas=batch_metas)
        else:
            collection.add(ids=batch_ids, documents=batch_docs, metadatas=batch_metas)

    print(f"已写入 Chroma collection={collection_name}，当前总数={collection.count()}")


def main() -> None:
    parser = argparse.ArgumentParser(description="把景区 Excel 转为知识块写入 knowledges.json，并可选写入 ChromaDB。")
    parser.add_argument(
        "--xlsx",
        default=r"D:\旅游助手\CnOpenData全国景区数据.xlsx",
        help="Excel 文件路径",
    )
    parser.add_argument(
        "--out-json",
        default=r"D:\旅游助手\chunks\knowledges.json",
        help="输出/合并的 knowledges.json 路径",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="只处理前 N 行（0 表示全部）",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="覆盖写入 out-json（默认是合并追加）",
    )
    parser.add_argument(
        "--no-chroma",
        action="store_true",
        help="只生成/合并 JSON，不写入 Chroma",
    )
    parser.add_argument("--chroma-host", default="192.168.2.5")
    parser.add_argument("--chroma-port", type=int, default=8083)
    parser.add_argument("--collection", default="collection_0424")
    args = parser.parse_args()

    new_chunks = build_chunks_from_xlsx(args.xlsx, limit=args.limit)
    if args.overwrite:
        merged = dedupe_chunks(new_chunks)
    else:
        existing = load_existing_chunks(args.out_json)
        merged = dedupe_chunks(existing + new_chunks)

    save_chunks(args.out_json, merged)
    print(f"已生成/合并 chunks：新增={len(new_chunks)}，合并后总数={len(merged)}")
    print(f"JSON 输出：{args.out_json}")

    if not args.no_chroma:
        add_chunks_to_chroma(
            new_chunks,
            host=args.chroma_host,
            port=args.chroma_port,
            collection_name=args.collection,
        )


if __name__ == "__main__":
    main()

