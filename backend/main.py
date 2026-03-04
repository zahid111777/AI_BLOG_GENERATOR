import os
from dotenv import load_dotenv
from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI

# ── Load environment ──────────────────────────────────────────────────────────
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "keys", ".env"))

# ── LLM ───────────────────────────────────────────────────────────────────────
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# ── State ─────────────────────────────────────────────────────────────────────
class BlogState(TypedDict):
    topic: str
    tone: str
    word_count: int
    title: str
    outline: List[str]
    content: str
    seo_keywords: List[str]
    meta_description: str


# ── Node 1 – Generate Title ───────────────────────────────────────────────────
def generate_title(state: BlogState) -> BlogState:
    prompt = (
        f"Generate one compelling, SEO-friendly blog post title for the topic: '{state['topic']}'. "
        f"The tone should be {state['tone']}. "
        "Return ONLY the title — no extra text, no quotes."
    )
    response = llm.invoke(prompt)
    state["title"] = response.content.strip()
    return state


# ── Node 2 – Generate Outline ─────────────────────────────────────────────────
def generate_outline(state: BlogState) -> BlogState:
    prompt = (
        f"Create a detailed blog post outline for the title: '{state['title']}'. "
        f"The tone should be {state['tone']} and the post should be around {state['word_count']} words. "
        "Return ONLY the outline as a numbered list of section headings (H2 level), "
        "one per line — no extra commentary."
    )
    response = llm.invoke(prompt)
    raw = response.content.strip()
    # Parse numbered lines into a clean list
    outline = [
        line.lstrip("0123456789). ").strip()
        for line in raw.splitlines()
        if line.strip()
    ]
    state["outline"] = outline
    return state


# ── Node 3 – Write Blog Content ───────────────────────────────────────────────
def write_blog(state: BlogState) -> BlogState:
    outline_text = "\n".join(f"{i+1}. {h}" for i, h in enumerate(state["outline"]))
    prompt = (
        f"Write a full, engaging blog post titled: '{state['title']}'. \n\n"
        f"Outline to follow:\n{outline_text}\n\n"
        f"Tone: {state['tone']}\n"
        f"Target length: approximately {state['word_count']} words.\n\n"
        "Format each section with its heading (using ##) followed by the paragraph(s). "
        "Include an introduction and a conclusion. "
        "Do NOT add any preamble or commentary — just the blog post."
    )
    response = llm.invoke(prompt)
    state["content"] = response.content.strip()
    return state


# ── Node 4 – SEO Optimization ─────────────────────────────────────────────────
def optimize_seo(state: BlogState) -> BlogState:
    prompt = (
        f"Given this blog post content:\n\n{state['content'][:1500]}...\n\n"
        "Return a JSON object with exactly two keys:\n"
        '  "keywords": a list of 5–8 SEO keywords (strings)\n'
        '  "meta_description": one sentence of 150–160 characters for the meta description\n'
        "Return ONLY valid JSON — no markdown fences, no extra text."
    )
    response = llm.invoke(prompt)
    import json, re
    raw = response.content.strip()
    # Strip markdown code fences if present
    raw = re.sub(r"^```[a-z]*\n?", "", raw)
    raw = re.sub(r"\n?```$", "", raw)
    try:
        data = json.loads(raw)
        state["seo_keywords"] = data.get("keywords", [])
        state["meta_description"] = data.get("meta_description", "")
    except json.JSONDecodeError:
        state["seo_keywords"] = []
        state["meta_description"] = ""
    return state


# ── Build LangGraph ───────────────────────────────────────────────────────────
def build_graph() -> StateGraph:
    workflow = StateGraph(BlogState)

    workflow.add_node("generate_title", generate_title)
    workflow.add_node("generate_outline", generate_outline)
    workflow.add_node("write_blog", write_blog)
    workflow.add_node("optimize_seo", optimize_seo)

    workflow.set_entry_point("generate_title")
    workflow.add_edge("generate_title", "generate_outline")
    workflow.add_edge("generate_outline", "write_blog")
    workflow.add_edge("write_blog", "optimize_seo")
    workflow.add_edge("optimize_seo", END)

    return workflow.compile()


graph = build_graph()


# ── Public API ────────────────────────────────────────────────────────────────
def generate_blog(topic: str, tone: str = "professional", word_count: int = 800) -> BlogState:
    """
    Run the full blog-generation pipeline.

    Parameters
    ----------
    topic      : The subject / topic for the blog post.
    tone       : Writing tone — e.g. 'professional', 'casual', 'technical', 'creative'.
    word_count : Target word count for the generated post.

    Returns
    -------
    A BlogState dict with keys: title, outline, content, seo_keywords, meta_description.
    """
    initial_state: BlogState = {
        "topic": topic,
        "tone": tone,
        "word_count": word_count,
        "title": "",
        "outline": [],
        "content": "",
        "seo_keywords": [],
        "meta_description": "",
    }
    result = graph.invoke(initial_state)
    return result


# ── Quick test ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    result = generate_blog("The Future of AI in Healthcare", tone="professional", word_count=600)
    print("Title :", result["title"])
    print("Outline:", result["outline"])
    print("\n--- CONTENT (first 300 chars) ---")
    print(result["content"][:300])
    print("\nSEO Keywords  :", result["seo_keywords"])
    print("Meta Description:", result["meta_description"])
