# OSH Law Chatbot v2

職業安全衛生法規查詢 GPT，整合 JSON 法規資料與 OpenAI 語意問答能力。

## 功能
- 自然語言輸入問題
- 根據內建 JSON 查詢最接近的條文與 GPT 解釋
- 支援多輪聊天

## 使用方法

1. 將 `職安法規整合版.json` 放在根目錄（已內含）
2. Streamlit Cloud 設定 Secrets：
   - `OPENAI_API_KEY = sk-xxxxx`
3. 部署並啟動 `app.py`
