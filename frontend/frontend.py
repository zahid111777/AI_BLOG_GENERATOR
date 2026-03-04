import sys
import os

# Allow importing from backend/
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
import markdown as md_parser
from backend.main import generate_blog

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Blog Generator",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
        html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

        .hero {
            background: linear-gradient(135deg, #6C63FF 0%, #3ECFCF 100%);
            border-radius: 18px;
            padding: 2.2rem 2.5rem;
            margin-bottom: 1.8rem;
            color: #fff;
        }
        .hero h1 {
            font-size: 2.6rem;
            font-weight: 800;
            margin: 0 0 0.4rem 0;
            line-height: 1.2;
            color: #fff !important;
        }
        .hero p {
            font-size: 1.05rem;
            opacity: 0.92;
            margin: 0;
            color: #fff !important;
        }

        .outline-card {
            display: flex;
            align-items: center;
            gap: 0.9rem;
            background: #f5f3ff;
            border-left: 5px solid #6C63FF;
            border-radius: 10px;
            padding: 0.9rem 1.2rem;
            margin-bottom: 0.7rem;
        }
        .outline-num {
            background: #6C63FF;
            color: #fff;
            font-weight: 700;
            font-size: 0.85rem;
            border-radius: 50%;
            min-width: 28px;
            height: 28px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .outline-text {
            font-size: 0.97rem;
            font-weight: 600;
            color: #1a1a2e;
        }

        .pill {
            display: inline-block;
            background: linear-gradient(90deg, #6C63FF22, #3ECFCF22);
            color: #4b3fc7;
            border: 1.5px solid #6C63FF55;
            border-radius: 999px;
            padding: 4px 14px;
            margin: 4px 3px;
            font-size: 0.82rem;
            font-weight: 500;
        }

        .meta-box {
            background: #f0fdfa;
            border: 1.5px solid #3ECFCF88;
            border-radius: 10px;
            padding: 1rem 1.2rem;
            font-size: 0.95rem;
            color: #134e4a;
            line-height: 1.6;
        }

        .stat-card {
            background: linear-gradient(135deg, #6C63FF11, #3ECFCF11);
            border: 1.5px solid #6C63FF30;
            border-radius: 12px;
            padding: 1rem;
            text-align: center;
        }
        .stat-num   { font-size: 2rem; font-weight: 800; color: #6C63FF; }
        .stat-label { font-size: 0.78rem; font-weight: 600; color: #555; text-transform: uppercase; letter-spacing: .06em; }

        section[data-testid="stSidebar"] {
            background: #fafafe;
            border-right: 1px solid #e9e6ff;
        }

        .stButton > button {
            background: linear-gradient(90deg, #6C63FF, #3ECFCF) !important;
            color: #fff !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 0.65rem 1.4rem !important;
            font-size: 1rem !important;
            font-weight: 700 !important;
            box-shadow: 0 4px 14px #6C63FF44;
            width: 100%;
        }
        .stButton > button:hover { opacity: 0.88; }

        .stTabs [data-baseweb="tab"] { font-weight: 600; font-size: 0.92rem; }
        .stTabs [aria-selected="true"] {
            color: #6C63FF !important;
            border-bottom: 2px solid #6C63FF !important;
        }

        .stDownloadButton > button {
            background: #fff !important;
            color: #6C63FF !important;
            border: 2px solid #6C63FF !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
        }

        .blog-content {
            background: #fff;
            border: 1px solid #e9e6ff;
            border-radius: 14px;
            padding: 2rem 2.4rem;
            line-height: 1.8;
            font-size: 1rem;
            color: #222;
        }
        /* Style rendered markdown inside the blog card */
        .blog-content h2 {
            color: #6C63FF;
            font-size: 1.35rem;
            font-weight: 700;
            margin-top: 1.6rem;
            margin-bottom: 0.4rem;
            border-bottom: 2px solid #e9e6ff;
            padding-bottom: 0.3rem;
        }
        .blog-content h3 {
            color: #3ECFCF;
            font-size: 1.1rem;
            font-weight: 600;
            margin-top: 1.2rem;
        }
        .blog-content p { margin-bottom: 0.9rem; }
        .blog-content strong { color: #1a1a2e; }
        .blog-content ul, .blog-content ol { padding-left: 1.5rem; margin-bottom: 0.9rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<p class="main-title">✍️ AI Blog Generator</p>', unsafe_allow_html=True)
# st.markdown(
#     "Loading...."
# )
st.divider()

# ── Sidebar – Controls ────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Blog Settings")
    st.markdown("---")

    topic = st.text_area(
        "📌 Blog Topic / Idea",
        placeholder="e.g. The Future of AI in Healthcare",
        height=110,
    )

    tone = st.selectbox(
        "🎨 Writing Tone",
        options=["Professional", "Casual", "Technical", "Creative", "Persuasive"],
        index=0,
    )

    word_count = st.slider(
        "📝 Target Word Count",
        min_value=300,
        max_value=2000,
        value=800,
        step=100,
        help="The AI will aim for this length.",
    )

    st.markdown("---")
    generate_btn = st.button("🚀 Generate Blog", use_container_width=True)
    st.caption("⏱️ Usually takes 20–40 seconds.")

# ── Main area ─────────────────────────────────────────────────────────────────
if generate_btn:
    if not topic.strip():
        st.warning("⚠️ Please enter a blog topic before generating.")
        st.stop()

    with st.spinner("✨ Crafting your blog post… hang tight!"):
        try:
            result = generate_blog(
                topic=topic.strip(),
                tone=tone.lower(),
                word_count=word_count,
            )
        except Exception as exc:
            st.error(f"❌ Generation failed: {exc}")
            st.stop()

    st.success("✅ Blog generated successfully!")

    # ── Tabs ──────────────────────────────────────────────────────────────────
    tab_blog, tab_outline, tab_seo = st.tabs(
        ["📄  Full Blog", "📋  Outline", "🔍  SEO Info"]
    )

    # ── Full Blog ─────────────────────────────────────────────────────────────
    with tab_blog:
        st.markdown(
            f"<h2 style='color:#6C63FF; margin-bottom:0.2rem;'>{result['title']}</h2>",
            unsafe_allow_html=True,
        )
        st.caption(f"Tone: **{tone}** &nbsp;|&nbsp; Target: **{word_count} words**")
        st.markdown("---")
        blog_html = md_parser.markdown(
            result["content"],
            extensions=["extra", "nl2br"],
        )
        st.markdown(
            f'<div class="blog-content">{blog_html}</div>',
            unsafe_allow_html=True,
        )
        st.markdown("<br>", unsafe_allow_html=True)
        md_content = f"# {result['title']}\n\n{result['content']}"
        st.download_button(
            label="⬇️ Download as Markdown",
            data=md_content,
            file_name=f"{result['title'][:50].replace(' ', '_')}.md",
            mime="text/markdown",
        )

    # ── Outline ───────────────────────────────────────────────────────────────
    with tab_outline:
        st.markdown(
            f"<h3 style='color:#6C63FF;'>Outline — <em>{result['title']}</em></h3>",
            unsafe_allow_html=True,
        )
        st.markdown("<br>", unsafe_allow_html=True)
        for i, section in enumerate(result["outline"], start=1):
            st.markdown(
                f"""
                <div class="outline-card">
                    <div class="outline-num">{i}</div>
                    <div class="outline-text">{section}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # ── SEO Info ──────────────────────────────────────────────────────────────
    with tab_seo:
        st.markdown(
            "<h3 style='color:#6C63FF;'>🔍 SEO Optimization</h3>",
            unsafe_allow_html=True,
        )
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("**📝 Meta Description**")
        st.markdown(
            f'<div class="meta-box">{result["meta_description"] or "N/A"}</div>',
            unsafe_allow_html=True,
        )
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("**🏷️ SEO Keywords**")
        if result["seo_keywords"]:
            pills = " ".join(
                f'<span class="pill">{kw}</span>' for kw in result["seo_keywords"]
            )
            st.markdown(pills, unsafe_allow_html=True)
        else:
            st.write("No keywords generated.")
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("**📊 Quick Stats**")
        word_actual = len(result["content"].split())
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(
                f'<div class="stat-card"><div class="stat-num">{word_actual}</div>'
                f'<div class="stat-label">Words</div></div>',
                unsafe_allow_html=True,
            )
        with c2:
            st.markdown(
                f'<div class="stat-card"><div class="stat-num">{len(result["outline"])}</div>'
                f'<div class="stat-label">Sections</div></div>',
                unsafe_allow_html=True,
            )
        with c3:
            st.markdown(
                f'<div class="stat-card"><div class="stat-num">{len(result["seo_keywords"])}</div>'
                f'<div class="stat-label">Keywords</div></div>',
                unsafe_allow_html=True,
            )

# ── Empty state ───────────────────────────────────────────────────────────────
else:
    st.markdown(
        """
        <div style="text-align:center; padding: 70px 20px;">
            <div style="font-size:4rem; margin-bottom:1rem;">✍️</div>
            <h3 style="color:#6C63FF; margin-bottom:0.5rem;">Ready to create your blog?</h3>
            <p style="color:#888; font-size:1rem; max-width:420px; margin:auto;">
                Fill in your topic, choose a tone and word count in the sidebar,
                then hit <strong>🚀 Generate Blog</strong> to get started.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
