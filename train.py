import streamlit as st
import subprocess

# 让用户输入 OpenAI API 密钥
api_key = st.text_input("请输入您的 OpenAI API 密钥")

# 检查 API 密钥的格式是否正确
if not api_key.startswith("sk-"):
    st.error("API 密钥格式不正确")

# 创建一个侧边栏，供用户选择 base model
base_model_options = ["ada", "babbage", "curie", "davinci", "自定义"]
base_model = st.sidebar.selectbox("选择要使用的 base model", base_model_options)

# 如果用户选择自定义，让用户输入 base model
if base_model == "自定义":
    base_model = st.sidebar.text_input("请输入自定义的 base model")

# 创建一个文本区域用于显示终端输出
terminal_output = st.text_area("终端输出", value="", height=200)

# 定义一个函数，用于将终端输出添加到文本区域中
def append_to_terminal_output(text):
    global terminal_output  # 声明为全局变量
    terminal_output += text
    st.text_area("终端输出", value=terminal_output, height=200)

# 让用户上传训练文件
train_file = st.file_uploader("上传训练文件", type="jsonl")

# 当用户点击“开始训练”按钮时触发的事件
if st.button("开始训练"):
    if train_file is not None:
        # 保存训练文件到本地
        with open("train.jsonl", "wb") as f:
            f.write(train_file.getvalue())

        # 使用 CLI 指令训练模型
        command = [
            "openai",
            "api",
            "fine_tunes.create",
            "-t",
            "train.jsonl",
            "-m",
            base_model
        ]

        # 执行命令并逐行读取输出
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        for line in process.stdout:
            append_to_terminal_output(line)

        # 等待命令执行完成
        process.wait()

        # 显示终端输出的文本
        append_to_terminal_output("命令执行完成。退出码：" + str(process.returncode))
