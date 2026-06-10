import os

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")


st.set_page_config(
    page_title="OpsAssist AI",
    page_icon="🛠️",
    layout="wide",
)

st.title("OpsAssist AI")
st.caption("RAG-based engineering support assistant with cited answers.")

question = st.text_area(
    "Ask a troubleshooting question",
    value="Why is the API Gateway returning 502 errors after release v2.3.1?",
    height=100,
)

top_k = st.slider("Number of documents to retrieve", min_value=1, max_value=10, value=3)

if st.button("Ask OpsAssist"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Retrieving context and generating answer..."):
            response = requests.post(
                f"{API_BASE_URL}/chat",
                json={
                    "question": question,
                    "top_k": top_k,
                },
                timeout=120,
            )

        if response.status_code != 200:
            st.error(f"Request failed: {response.status_code}")
            st.code(response.text)
        else:
            data = response.json()

            st.subheader("Answer")
            st.write(data["answer"])

            col1, col2 = st.columns(2)

            with col1:
                st.metric("Confidence", data["confidence"])

            with col2:
                st.write("**Escalation**")
                st.write(data.get("escalation") or "Not required")

            st.subheader("Sources")

            for index, source in enumerate(data["sources"], start=1):
                with st.expander(f"Source {index}: {source['document']}"):
                    st.write(f"**Chunk ID:** {source.get('chunk_id')}")
                    st.write(f"**Score:** {source.get('score')}")
                    st.write(source.get("content_preview", ""))