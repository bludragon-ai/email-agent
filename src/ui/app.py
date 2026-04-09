"""Streamlit UI for Email Agent."""

from __future__ import annotations

import streamlit as st

from src.providers.local import LocalEmailProvider
from src.agents.email_agent import EmailAgent
from src.models.email import EmailCategory, EmailPriority

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------

st.set_page_config(page_title="Email Agent", page_icon="📧", layout="wide")


@st.cache_resource
def _agent() -> EmailAgent:
    return EmailAgent(provider=LocalEmailProvider())


agent = _agent()

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------

st.sidebar.title("📧 Email Agent")
st.sidebar.caption("AI-powered email triage & management")

view = st.sidebar.radio("View", ["Inbox", "Compose"], index=0)

CATEGORY_COLORS = {
    EmailCategory.URGENT: "🔴",
    EmailCategory.CLIENT: "🔵",
    EmailCategory.ROUTINE: "⚪",
    EmailCategory.NEWSLETTER: "🟢",
    EmailCategory.SPAM: "⚠️",
}

PRIORITY_LABELS = {
    EmailPriority.CRITICAL: "🔴 Critical",
    EmailPriority.HIGH: "🟠 High",
    EmailPriority.MEDIUM: "🟡 Medium",
    EmailPriority.LOW: "🔵 Low",
    EmailPriority.MINIMAL: "⚪ Minimal",
}

# ---------------------------------------------------------------------------
# Inbox View
# ---------------------------------------------------------------------------

if view == "Inbox":
    st.title("📥 Inbox")

    emails = agent.inbox(limit=50)

    if not emails:
        st.info("No emails found.")
        st.stop()

    # Email list
    for email in emails:
        read_indicator = "" if email.is_read else "● "
        col1, col2, col3 = st.columns([0.5, 3, 1])
        with col1:
            st.write(read_indicator)
        with col2:
            if st.button(
                f"**{email.subject}**  \n_{email.from_addr}_",
                key=f"email_{email.id}",
                use_container_width=True,
            ):
                st.session_state["selected_email"] = email.id
                agent.mark_read(email.id)
        with col3:
            st.caption(email.date.strftime("%b %d %H:%M"))

    st.divider()

    # Detail pane
    selected_id = st.session_state.get("selected_email")
    if selected_id:
        email = agent.get_email(selected_id)
        if email:
            st.subheader(email.subject)
            st.caption(f"From: {email.from_addr} — {email.date.strftime('%Y-%m-%d %H:%M UTC')}")
            st.text(email.body)

            st.divider()

            # AI Analysis
            if st.button("🤖 Analyze with AI", key="analyze_btn"):
                with st.spinner("Analyzing…"):
                    analysis = agent.analyze(email.id)
                st.session_state["analysis"] = analysis

            analysis = st.session_state.get("analysis")
            if analysis and analysis.email_id == selected_id:
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Category", f"{CATEGORY_COLORS.get(analysis.category, '')} {analysis.category.value}")
                with col2:
                    st.metric("Priority", PRIORITY_LABELS.get(analysis.priority, str(analysis.priority)))

                st.info(f"**Summary:** {analysis.summary}")
                if analysis.key_points:
                    st.write("**Key points:**")
                    for kp in analysis.key_points:
                        st.write(f"- {kp}")
                st.write(f"**Suggested action:** {analysis.suggested_action}")
                st.write(f"**Requires reply:** {'Yes' if analysis.requires_reply else 'No'}")

            st.divider()

            # Thread summary
            thread = agent.get_thread(email.thread_id)
            if len(thread) > 1:
                if st.button("📝 Summarize Thread", key="summarize_btn"):
                    with st.spinner("Summarizing thread…"):
                        summary = agent.summarize_thread(email.thread_id)
                    st.session_state["thread_summary"] = (email.thread_id, summary)

                ts = st.session_state.get("thread_summary")
                if ts and ts[0] == email.thread_id:
                    st.success(ts[1])

            # Draft reply
            st.subheader("✍️ Draft Reply")
            tone = st.selectbox("Tone", ["professional", "friendly", "formal", "concise", "apologetic"], key="tone_select")
            extra = st.text_area("Additional instructions (optional)", key="reply_instructions")
            if st.button("Generate Reply", key="draft_btn"):
                with st.spinner("Drafting reply…"):
                    draft = agent.draft_reply(email.id, tone=tone, instructions=extra)
                st.session_state["draft"] = draft

            draft = st.session_state.get("draft")
            if draft and draft.email_id == selected_id:
                st.text_area("Draft", value=draft.body, height=200, key="draft_output")
                st.caption(f"Confidence: {draft.confidence:.0%}")

# ---------------------------------------------------------------------------
# Compose View
# ---------------------------------------------------------------------------

elif view == "Compose":
    st.title("✉️ Compose")
    to = st.text_input("To")
    subject = st.text_input("Subject")
    body = st.text_area("Body", height=300)

    if st.button("Send"):
        if to and subject and body:
            agent.send_email(to, subject, body)
            st.success("Email sent (demo).")
        else:
            st.warning("Fill in all fields.")
