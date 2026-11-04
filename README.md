# 边界旅行

uni-app 前端和 Django 后端组成的旅游助手。首页可以浏览国内、国外景点，登录后可以和 AI 对话。对话会检索本地景区知识，并按问题补充实时天气和附近地点。

## 目录

- `旅游助手/`：uni-app（Vue 3）客户端。底部四个页签是首页、国内、国外、我的。
- `服务器端/llm_server/`：Django 项目。用户接口在 `/user/`，对话接口在 `/api/`。
- `chunks/knowledges.json`：已经切好的景区知识片段。
- `chromadb/`：本地向量库数据，集合名是 `collection_0424`。
- `CnOpenData全国景区数据（样本）.xlsx`：景区样本表。
- `xlsx_景区数据_to_chunks_and_chroma.py`：把样本表整理成知识片段。
- `词向量数据库_添加.py`、`词向量数据库_查询.py`、`词向量数据库_删除.py`：维护上面的向量集合。
- `语义分割.py`、`读取md文档用于语义分割.py`：用 `segmentation_models/` 做中文文档切分。

## 没有放进仓库的内容

这些文件太大，或者包含本机密钥和用户数据：

- `bge-reranker-base` 的权重：`pytorch_model.bin`、`model.safetensors`、`onnx/model.onnx`。配置和分词器仍在 `服务器端/llm_server/models/`。
- 文档分割模型的 `segmentation_models/pytorch_model.bin`。
- `服务器端/llm_server/travelassistant/.env` 里的天气、地图密钥。
- 用户上传的图片、头像和 `db.sqlite3`。业务数据使用 MySQL。

## 后端

在 MySQL 中创建数据库 `travel_assistant`，字符集用 `utf8mb4`。数据库地址和库名写在 `服务器端/llm_server/aisite/settings.py`，默认连本机 `3306`。密码从环境变量读取。

在 `服务器端/llm_server/.env` 或 `服务器端/llm_server/travelassistant/.env` 写入：

```env
DASHSCOPE_API_KEY=
WEATHER_API_KEY=
AMAP_API_KEY=
DJANGO_SECRET_KEY=
JWT_SECRET=
DB_PASSWORD=
```

`DASHSCOPE_API_KEY` 用于通义千问和文本向量，`WEATHER_API_KEY` 用于心知天气，`AMAP_API_KEY` 用于高德地理编码和附近搜索。

主要依赖：Django 5.2、`django-cors-headers`、PyJWT、Pillow、`openai`、`chromadb`、`sentence-transformers`、`httpx`，以及连接 MySQL 的驱动。进入项目目录后执行迁移并启动，端口要和前端一致：

```powershell
cd 服务器端\llm_server
python manage.py migrate
python manage.py runserver 8081
```

重排序模型是 `BAAI/bge-reranker-base`。把权重放到 `服务器端/llm_server/models/`，和现有的 `config.json`、分词器放在一起。文档分割模型来自 ModelScope 的 `iic/nlp_bert_document-segmentation_chinese-base`，权重放到 `segmentation_models/`。

接口：

- `POST /user/register/`、`POST /user/login/`：注册和登录，登录后返回 JWT。
- `POST /user/profile/`、`POST /user/update_profile/`、`POST /user/upload_avatar/`：个人资料和头像。
- `POST /api/ai/`：流式对话。可附带深度思考、联网搜索和图片。
- `POST /api/upload/`：上传对话图片。
- `POST /api/history/`、`POST /api/detail/`、`POST /api/deltopic/`：话题列表、详情和删除。

除登录、注册、后台和静态文件外，请求需要带 `Authorization: Bearer <token>`。

## 前端

用 HBuilderX 打开 `旅游助手/`。接口地址在 `旅游助手/common/config.js`，当前是 `http://localhost:8081`。个人中心页面里还有一处写死的 `http://127.0.0.1:8081`，换服务器时两处一起改。

运行到浏览器后，从首页进入 AI 对话。未登录会先到登录页。

## 重建知识库

样本表更新后，在仓库根目录执行 `xlsx_景区数据_to_chunks_and_chroma.py` 生成 `chunks/knowledges.json`，再执行 `词向量数据库_添加.py` 写入 Chroma。Markdown 文档可以放到 `data/`，用 `读取md文档用于语义分割.py` 切分。这两个向量脚本和对话检索都读取环境变量 `DASHSCOPE_API_KEY`。
