import os
import re
import json
from modelscope.outputs import OutputKeys
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks

# --- 1. 初始化模型流水线 ---
p = pipeline(
    task=Tasks.document_segmentation,
    model='./segmentation_models', 
    model_revision='master'
)

# --- 2. 工具函数 ---
DOT_PLACEHOLDER = "__DOT__"

def protect_dots(text):
    """保护数字间的点（如 2025.6.1）"""
    return re.sub(r'(\d)\.(\d)', r'\1' + DOT_PLACEHOLDER + r'\2', text)

def restore_dots(text):
    """还原保护符号"""
    return text.replace(DOT_PLACEHOLDER, ".")

# --- 3. 核心处理函数 ---
def process_segmentation():
    folder_path = r'D:\旅游助手\data'
    output_dir = "./chunks"
    MIN_CHUNK_LENGTH = 120  # 设定最小长度限制
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    knowledge_chunks = []

    if not os.path.exists(folder_path):
        print(f"错误：找不到目录 {folder_path}")
        return

    files = [f for f in os.listdir(folder_path) if f.endswith(".md")]

    for file in files:
        file_path = os.path.join(folder_path, file)
        print(f"正在处理: {file}")
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            protected_content = protect_dots(content)
            result = p(documents=protected_content)
            raw_text = result[OutputKeys.TEXT].strip()
            
            # 原始分段
            raw_chunks = raw_text.split('\n')

            # --- 长度限制逻辑：累加逻辑 ---
            buffer_content = ""
            for chunk in raw_chunks:
                clean_chunk = chunk.strip()
                if not clean_chunk:
                    continue
                
                # 如果当前 buffer 不为空，加个空格或换行再拼接
                if buffer_content:
                    buffer_content += " " + clean_chunk
                else:
                    buffer_content = clean_chunk
                
                # 检查长度是否达到要求
                if len(buffer_content) >= MIN_CHUNK_LENGTH:
                    knowledge_chunks.append({
                        "metadata": {
                            "source": file,
                            "department": "研发部",
                        },
                        "content": restore_dots(buffer_content)
                    })
                    buffer_content = "" # 重置缓冲区
            
            # 文件处理完后，如果 buffer 里还有剩下的内容（不足120），也强行存入或丢弃
            if buffer_content:
                knowledge_chunks.append({
                    "metadata": {
                        "source": file,
                        "department": "研发部",
                    },
                    "content": restore_dots(buffer_content)
                })

        except Exception as e:
            print(f"处理文件 {file} 时出错: {e}")

    # 4. 写入 JSON
    output_file = os.path.join(output_dir, "knowledges.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(knowledge_chunks, f, ensure_ascii=False, indent=4)
        
    print("-" * 30)
    print(f"处理完成！生成知识块总数: {len(knowledge_chunks)}")
    print(f"保存路径: {output_file}")

if __name__ == '__main__':
    process_segmentation()