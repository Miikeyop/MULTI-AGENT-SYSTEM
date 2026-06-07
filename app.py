import streamlit as st
import time
from pipeline import result_report_pipeline

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchMind · Multi-Agent",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

/* ── Root tokens ── */
:root {
    --bg:          #0a0c10;
    --surface:     #111318;
    --border:      #1e2230;
    --accent:      #00e5a0;
    --accent2:     #0070f3;
    --accent3:     #ff6b35;
    --text:        #e8eaf0;
    --muted:       #5a6070;
    --card-bg:     #13161e;
}

/* ── Global reset ── */
html, body, .stApp {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'DM Mono', monospace;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem 4rem !important; max-width: 1100px !important; }

/* ── Hero header ── */
.hero {
    text-align: center;
    padding: 3rem 0 2rem;
    position: relative;
}
.hero-tag {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.25em;
    color: var(--accent);
    text-transform: uppercase;
    margin-bottom: 0.75rem;
}
.hero h1 {
    font-family: 'Syne', sans-serif !important;
    font-size: clamp(2.4rem, 5vw, 3.6rem) !important;
    font-weight: 800 !important;
    color: var(--text) !important;
    letter-spacing: -0.03em;
    line-height: 1.1;
    margin: 0 0 0.5rem !important;
}
.hero h1 span { color: var(--accent); }
.hero-sub {
    color: var(--muted);
    font-size: 0.88rem;
    letter-spacing: 0.04em;
}

/* ── Input card ── */
.input-card {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 2rem 2.2rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.input-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
}

/* ── Streamlit input override ── */
.stTextInput > div > div > input {
    background: #0d1017 !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.92rem !important;
    padding: 0.75rem 1rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(0,229,160,0.15) !important;
}
.stTextInput label {
    color: var(--muted) !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
}

/* ── Button ── */
.stButton > button {
    width: 100% !important;
    background: var(--accent) !important;
    color: #000 !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.7rem !important;
    transition: opacity 0.2s, transform 0.15s !important;
    cursor: pointer !important;
}
.stButton > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── Pipeline step cards ── */
.step-card {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1.2rem;
    position: relative;
    overflow: hidden;
}
.step-card.active  { border-color: var(--accent);  }
.step-card.done    { border-color: #1a3a2a; }
.step-card.pending { opacity: 0.4; }

.step-card::after {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(0,229,160,0.03) 0%, transparent 60%);
    pointer-events: none;
}
.step-card.active::after  { background: linear-gradient(135deg, rgba(0,229,160,0.06) 0%, transparent 60%); }
.step-card.done::after    { background: linear-gradient(135deg, rgba(0,229,160,0.02) 0%, transparent 60%); }

.step-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 0.5rem;
}
.step-num {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    color: var(--muted);
    letter-spacing: 0.1em;
    min-width: 28px;
}
.step-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.95rem;
    font-weight: 700;
    color: var(--text);
    letter-spacing: -0.01em;
}
.step-badge {
    margin-left: auto;
    font-size: 0.65rem;
    font-family: 'DM Mono', monospace;
    letter-spacing: 0.08em;
    padding: 0.2rem 0.55rem;
    border-radius: 20px;
}
.badge-active  { background: rgba(0,229,160,0.15); color: var(--accent); }
.badge-done    { background: rgba(0,229,160,0.08); color: #3aaa78; }
.badge-pending { background: rgba(90,96,112,0.15); color: var(--muted); }

.step-desc {
    font-size: 0.75rem;
    color: var(--muted);
    margin-left: 38px;
    letter-spacing: 0.02em;
    line-height: 1.6;
}

/* ── Pulse animation ── */
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.4} }
.pulsing { animation: pulse 1.4s ease-in-out infinite; }

/* ── Result sections ── */
.result-section {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.8rem 2rem;
    margin-bottom: 1.4rem;
}
.result-section-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.result-section-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
}
.result-content {
    font-family: 'DM Mono', monospace;
    font-size: 0.82rem;
    color: #b0b8cc;
    line-height: 1.8;
    white-space: pre-wrap;
    word-break: break-word;
}

/* ── Error box ── */
.error-box {
    background: rgba(255,60,60,0.08);
    border: 1px solid rgba(255,60,60,0.25);
    border-radius: 10px;
    padding: 1rem 1.2rem;
    color: #ff6b6b;
    font-family: 'DM Mono', monospace;
    font-size: 0.8rem;
    line-height: 1.6;
}

/* ── Footer ── */
.footer {
    text-align: center;
    color: var(--muted);
    font-size: 0.7rem;
    letter-spacing: 0.08em;
    padding-top: 3rem;
    border-top: 1px solid var(--border);
    margin-top: 3rem;
}

/* ── Divider ── */
hr { border-color: var(--border) !important; margin: 2rem 0 !important; }

/* Remove Streamlit expander arrow styles bleeding through */
.streamlit-expanderHeader { font-family: 'Syne', sans-serif !important; }
</style>
""", unsafe_allow_html=True)


# ── Helper: render pipeline step ─────────────────────────────────────────────
def step_card(num: str, title: str, desc: str, status: str):
    badge_class = f"badge-{status}"
    badge_text  = {"active": "● RUNNING", "done": "✓ DONE", "pending": "○ WAITING"}[status]
    card_class  = f"step-card {status}"
    pulse_class = "pulsing" if status == "active" else ""

    st.markdown(f"""
    <div class="{card_class}">
        <div class="step-header">
            <span class="step-num">{num}</span>
            <span class="step-title {pulse_class}">{title}</span>
            <span class="step-badge {badge_class}">{badge_text}</span>
        </div>
        <div class="step-desc">{desc}</div>
    </div>
    """, unsafe_allow_html=True)


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-tag">⬡ Multi-Agent Research System</div>
    <h1>Research<span>Mind</span></h1>
    <div class="hero-sub">web search · deep reading · report generation · critic review</div>
</div>
""", unsafe_allow_html=True)

# ── Input card ───────────────────────────────────────────────────────────────
st.markdown('<div class="input-card">', unsafe_allow_html=True)
topic = st.text_input(
    "Research Topic",
    placeholder="e.g. 'Latest advancements in quantum computing 2025'",
    key="topic_input",
)
run_btn = st.button("⚡  Launch Pipeline", key="run_btn")
st.markdown('</div>', unsafe_allow_html=True)

# ── Pipeline status ───────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.markdown('<div class="error-box">⚠ Please enter a research topic before launching.</div>', unsafe_allow_html=True)
    else:
        # Define the 4 stages
        stages = [
            ("01", "Web Search Agent",    "Queries the web for recent, reliable information on the topic."),
            ("02", "Reader Agent",         "Selects the best URL, scrapes full content, and extracts research notes."),
            ("03", "Report Generator",     "Synthesises search results + scraped content into a structured report."),
            ("04", "Critic & Reviewer",    "Evaluates the report for accuracy, depth, and improvement areas."),
        ]

        status_area = st.empty()

        def render_stages(current: int):
            html = ""
            for i, (num, title, desc) in enumerate(stages):
                if i < current:
                    s = "done"
                elif i == current:
                    s = "active"
                else:
                    s = "pending"
                badge_class = f"badge-{s}"
                badge_text  = {"active": "● RUNNING", "done": "✓ DONE", "pending": "○ WAITING"}[s]
                card_class  = f"step-card {s}"
                pulse_class = "pulsing" if s == "active" else ""
                html += f"""
                <div class="{card_class}">
                    <div class="step-header">
                        <span class="step-num">{num}</span>
                        <span class="step-title {pulse_class}">{title}</span>
                        <span class="step-badge {badge_class}">{badge_text}</span>
                    </div>
                    <div class="step-desc">{desc}</div>
                </div>"""
            status_area.markdown(html, unsafe_allow_html=True)

        # ── Run pipeline with live status ──────────────────────────────────
        render_stages(0)

        try:
            import threading

            result_holder = {}
            error_holder  = {}
            stage_holder  = {"current": 0}

            # Monkey-patch print to track stage transitions
            import builtins
            _orig_print = builtins.print
            stage_keywords = ["web agent is working", "reader agent is working",
                              "report is working", "reviewing report is working"]
            stage_idx = [0]

            def _tracked_print(*args, **kwargs):
                _orig_print(*args, **kwargs)
                msg = " ".join(str(a) for a in args).lower()
                for i, kw in enumerate(stage_keywords):
                    if kw in msg and stage_holder["current"] <= i:
                        stage_holder["current"] = i

            builtins.print = _tracked_print

            def _run():
                try:
                    result_holder["state"] = result_report_pipeline(topic.strip())
                except Exception as e:
                    error_holder["err"] = str(e)

            t = threading.Thread(target=_run, daemon=True)
            t.start()

            while t.is_alive():
                render_stages(stage_holder["current"])
                time.sleep(0.6)

            builtins.print = _orig_print

            if "err" in error_holder:
                raise RuntimeError(error_holder["err"])

            render_stages(4)   # all done

            state = result_holder["state"]

            # ── Results ───────────────────────────────────────────────────
            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown("""
            <div style="font-family:'Syne',sans-serif;font-size:1.35rem;font-weight:800;
                        color:#e8eaf0;letter-spacing:-0.02em;margin-bottom:1.4rem;">
                📄 Pipeline Output
            </div>
            """, unsafe_allow_html=True)

            sections = [
                ("🔍  Search Results",     "search_result"),
                ("📖  Reader Notes",        "reader_result"),
                ("📝  Generated Report",    "report"),
                ("🔎  Critic Feedback",     "feedback"),
            ]

            for label, key in sections:
                content = state.get(key, "")
                if hasattr(content, "content"):
                    content = content.content
                if not content:
                    continue
                with st.expander(label, expanded=(key == "report")):
                    st.markdown(f'<div class="result-content">{content}</div>',
                                unsafe_allow_html=True)

        except Exception as e:
            st.markdown(
                f'<div class="error-box">🚨 Pipeline error:<br><br>{e}</div>',
                unsafe_allow_html=True
            )

# ── Idle state: show skeleton stages ─────────────────────────────────────────
elif not run_btn:
    stages_static = [
        ("01", "Web Search Agent",    "Queries the web for recent, reliable information on the topic."),
        ("02", "Reader Agent",         "Selects the best URL, scrapes full content, and extracts research notes."),
        ("03", "Report Generator",     "Synthesises search results + scraped content into a structured report."),
        ("04", "Critic & Reviewer",    "Evaluates the report for accuracy, depth, and improvement areas."),
    ]
    html = ""
    for num, title, desc in stages_static:
        html += f"""
        <div class="step-card pending">
            <div class="step-header">
                <span class="step-num">{num}</span>
                <span class="step-title">{title}</span>
                <span class="step-badge badge-pending">○ WAITING</span>
            </div>
            <div class="step-desc">{desc}</div>
        </div>"""
    st.markdown(html, unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    RESEARCHMIND · MULTI-AGENT PIPELINE · POWERED BY LangGraph
</div>
""", unsafe_allow_html=True)