import streamlit as st
import openai
from openai import OpenAI
import json
import difflib

openai.__version__ = "1.3.7"

# 初始化 client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 讀取法規 JSON
@st.cache_data
def load_laws():
    with open("職安法規整合版.json", "r", encoding="utf-8") as f:
        return json.load(f)

law_data = load_laws()

st.set_page_config(page_title="職安法規查詢 GPT", page_icon="⚖️")
st.title("⚖️ 職安法規查詢 GPT")

# 聊天記錄初始化
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "你是台灣職業安全衛生法規專家，請依據下列條文回答問題。"}
    ]

# 顯示歷史訊息
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["content"])

# 查找最相關的法條（模糊語意比對）
def search_law(query):
    contents = [(item.get("法條內容", "") + " " + item.get("GPT回應版本", "")) for item in law_data]
    matches = difflib.get_close_matches(query, contents, n=1, cutoff=0.1)
    if not matches:
        return None
    for item in law_data:
        full = item.get("法條內容", "") + " " + item.get("GPT回應版本", "")
        if matches[0] in full:
            return item
    return None

# 使用者提問
if query := st.chat_input("請輸入您的職安法規問題"):
    st.chat_message("user").markdown(query)
    st.session_state.messages.append({"role": "user", "content": query})

    matched_law = search_law(query)
    context = ""
    if matched_law:
        context = f"【相關條文】\n{matched_law.get('法條編號')} {matched_law.get('法條標題')}\n{matched_law.get('法條內容')}\n\nGPT解釋：{matched_law.get('GPT回應版本')}"
    else:
        context = "查無對應法條，請直接回答問題。"

    st.chat_message("assistant").markdown(f"正在查詢...

{context}")

    # 傳給 GPT
    messages = st.session_state.messages + [{"role": "system", "content": context}]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.3
    )
    reply = response.choices[0].message.content
    st.chat_message("assistant").markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})
