import os
import streamlit as st
import requests
import json
from pathlib import Path
from datetime import datetime
import uuid

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="ShramikSathi",
    page_icon="⚖️",
    layout="wide"
)

st.title("⚖️ ShramikSathi")
st.caption("Your Labour Law Assistant")

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT.parent / "Day-03" / "data" / "records.json"
FEEDBACK_FILE = ROOT / "data" / "feedback.jsonl"

FEEDBACK_FILE.parent.mkdir(parents=True, exist_ok=True)

# ---------------- LOAD FAQ DATA ----------------

with open(DATA_FILE, encoding="utf-8") as f:
    faqs = json.load(f)

# ---------------- OLD LAW MAPPING ----------------

OLD_LAWS = {
    "gratuity": (
        "Payment of Gratuity Act, 1972",
        "Code on Social Security, 2020"
    ),
    "minimum wage": (
        "Minimum Wages Act, 1948",
        "Code on Wages, 2019"
    ),
    "esi": (
        "Employees' State Insurance Act, 1948",
        "Code on Social Security, 2020"
    )
}


def get_law_mapping(question):
    q = question.lower()

    for key, value in OLD_LAWS.items():
        if key in q:
            return value

    return (
        "Old Act mapping not specified",
        "Applicable Labour Code"
    )


# ---------------- FAQ MATCHING ----------------

def get_faq(question):
    q = question.lower()

    for faq in faqs:
        faq_question = faq.get("question", "").lower()

        if q in faq_question or faq_question in q:
            return faq

    keywords = {
        "gratuity": ["gratuity"],
        "wage": ["wages", "wage"],
        "esi": ["esi"],
        "worker": ["worker", "osh"]
    }

    for key, words in keywords.items():
        if any(word in q for word in words):
            for faq in faqs:
                if any(word in faq.get("question", "").lower()
                       for word in words):
                    return faq

    return None


# ---------------- FEEDBACK ----------------

def save_feedback(question, answer, rating):
    record = {
        "question": question,
        "answer": answer,
        "rating": rating,
        "timestamp": datetime.now().isoformat()
    }

    with open(FEEDBACK_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def feedback_callback(question, answer, rating):
    save_feedback(question, answer, rating)
    st.session_state.feedback_notice = "Feedback saved successfully!"


# ---------------- SESSION STATE ----------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

if "feedback_notice" not in st.session_state:
    st.session_state.feedback_notice = ""


# ---------------- SIDEBAR ----------------

mode = st.sidebar.selectbox(
    "Choose Assistant",
    ["RAG", "Agent"]
)

default_url = (
    os.getenv("RAG_API_URL", "http://127.0.0.1:8008")
    if mode == "RAG"
    else os.getenv("AGENT_API_URL", "http://127.0.0.1:8009")
)

api_url = st.sidebar.text_input("API URL", default_url)

if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
    st.session_state.thread_id = str(uuid.uuid4())
    st.rerun()


# ---------------- DISPLAY CHAT HISTORY ----------------

for i, msg in enumerate(st.session_state.messages):

    with st.chat_message(msg["role"]):
        st.write(msg["content"])

        if msg["role"] == "assistant":

            if msg.get("old_law"):
                st.info(
                    f"Old Law: {msg['old_law']} → "
                    f"New Code: {msg['new_code']}"
                )

            if msg.get("faq_date"):
                st.caption("FAQ Date: " + msg["faq_date"])

            citations = msg.get("citations", [])

            if citations:
                st.subheader("📚 Sources")

                for j, citation in enumerate(citations, 1):
                    with st.expander(f"Source {j}: {citation.get('title', 'Document')}"):
                        st.write("File:", citation.get("source", "N/A"))
                        st.write("Page:", citation.get("page", "N/A"))

            col1, col2 = st.columns(2)

            col1.button(
                "👍 Helpful",
                key=f"up_{i}",
                on_click=feedback_callback,
                args=(msg["question"], msg["content"], "up")
            )

            col2.button(
                "👎 Not Helpful",
                key=f"down_{i}",
                on_click=feedback_callback,
                args=(msg["question"], msg["content"], "down")
            )


# ---------------- FEEDBACK MESSAGE ----------------

if st.session_state.feedback_notice:
    st.success(st.session_state.feedback_notice)
    st.session_state.feedback_notice = ""


# ---------------- CHAT INPUT ----------------

question = st.chat_input("Ask your labour law question...")

if question:

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.write(question)

    endpoint = "/ask" if mode == "RAG" else "/agent"

    payload = {"question": question}

    if mode == "Agent":
        payload.update({
            "thread_id": st.session_state.thread_id,
            "approved": None
        })

    try:
        response = requests.post(
            api_url.rstrip("/") + endpoint,
            json=payload,
            timeout=60
        )

        response.raise_for_status()
        result = response.json()

        answer = result.get("answer", "No answer returned.")

        # Agent approval response
        if result.get("approval_required"):
            st.warning("Approval required for calculation.")
            answer = "Calculation requires your approval. Please use the Agent API approval workflow."

        faq = get_faq(question)

        old_law, new_code = get_law_mapping(question)

        citations = result.get("citations", [])

        # ---------------- DISPLAY ANSWER ----------------

        with st.chat_message("assistant"):

            st.write(answer)

            st.info(
                f"Old Law: {old_law} → New Code: {new_code}"
            )

            if faq:
                st.caption("FAQ Date: " + faq.get("faq_date", "N/A"))

            if citations:
                st.subheader("📚 Sources")

                for j, citation in enumerate(citations, 1):
                    with st.expander(f"Source {j}: {citation.get('title', 'Document')}"):
                        st.write("File:", citation.get("source", "N/A"))
                        st.write("Page:", citation.get("page", "N/A"))

        # ---------------- SAVE CHAT ----------------

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer,
            "question": question,
            "old_law": old_law,
            "new_code": new_code,
            "faq_date": faq.get("faq_date") if faq else None,
            "citations": citations
        })

        st.rerun()

    except requests.RequestException as e:
        st.error(f"API connection error: {e}")

    except Exception as e:
        st.error(f"Something went wrong: {e}")
