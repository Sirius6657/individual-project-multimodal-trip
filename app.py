from dotenv import load_dotenv
import os
import streamlit as st

load_dotenv(override=True)  # 本地：读 .env；云端：没有这个文件，自动跳过，不报错


def get_key(name: str):
    """兼容写法：本地从 .env 读，云端从 Streamlit Secrets 读——同一份代码两处都能跑"""
    value = os.getenv(name)        # ① 先试本地：.env 已被 load_dotenv 装进环境变量
    if value:
        return value
    try:
        return st.secrets[name]    # ② 再试云端：从平台 Secrets 读
    except Exception:
        return None                # ③ 两处都没有 → 返回 None，交给下面的提示逻辑


def key_source(name: str) -> str:
    """只报「从哪条通道取到的」，用于排障；绝不显示密钥本身的值"""
    if os.getenv(name):
        return "本地 .env"
    try:
        st.secrets[name]
        return "云端 Secrets"
    except Exception:
        return "都没有"


DEEPSEEK_API_KEY = get_key("DEEPSEEK_API_KEY")

st.title("我的第一个云端应用")
st.write("这是我在数据分析课上部署的第一个 Streamlit 应用。")

years = st.slider("投资年限（年）", 1, 30, 10)
rate = st.slider("年化收益率（%）", 1, 20, 5)
result = 10000 * (1 + rate / 100) ** years
st.metric("1 万元到期本息", f"{result:,.0f} 元")

with st.sidebar.expander("🔧 密钥体检（部署排障用）"):
    st.write("DEEPSEEK_API_KEY：", "已配置" if DEEPSEEK_API_KEY else "❌ 缺失")
    st.caption(f"密钥来源：{key_source('DEEPSEEK_API_KEY')}")
