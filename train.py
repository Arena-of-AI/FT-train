import streamlit as st
import subprocess
import openai

# 让用户输入 API 密钥
api_key = st.text_input("请输入您的 OpenAI API 密钥")

# 检查API密钥的格式是否正确
if not api_key.startswith("sk"):
    st.error("API密钥格式不正确")

# 设置 OpenAI API 密钥
openai.api_key = api_key

# 获取以前的模型列表
models = openai.FineTune.list()

# 提取模型名称列表
model_names = [model["display_name"] for model in models["data"]]

# 添加系统默认模型
model_names.append("System Default")

# 创建一个下拉选择框，供用户选择模型
selected_model = st.selectbox("选择要训练的模型", model_names)

# 让用户上传.jsonl文件
uploaded_file = st.file_uploader("上传.jsonl文件", type="jsonl")

if uploaded_file:
    # 将文件保存到本地
    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # 使用CLI指令训练模型
    command = [
        "openai",
        "api",
        "fine_tunes.create",
        "-t",
        uploaded_file.name,
        "-m",
        selected_model
    ]

    # 执行命令并捕获输出
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    # 显示终端输出的文本
    if stderr:
        st.error(stderr.decode())
    else:
        st.code(stdout.decode())
