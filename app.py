import gradio as gr
from query import ask


def handle_query(question):
    if not question.strip():
        return "Please enter a question.", ""

    result = ask(question)
    sources = "\n".join(f"• {source}" for source in result["sources"])

    return result["answer"], sources


css = """
.gradio-container {
    max-width: 1050px !important;
    margin: auto !important;
}
"""


with gr.Blocks(
    theme=gr.themes.Soft(),
    title="MSDS Unofficial Guide"
) as demo:

    gr.Markdown("""
# 🎓 UT Austin MSDS Unofficial Guide

Ask questions about:

- 📚 Courses  
- 👨‍🏫 Professors  
- ⏰ Workload  
- 📈 Difficulty  
- 🎯 Admissions  

Answers are generated from collected student reviews and program documents.
""")

    question = gr.Textbox(
        label="Your Question",
        placeholder="Example: Which courses are the hardest?",
        lines=2
    )

    ask_button = gr.Button(
        "🔍 Ask the Guide",
        variant="primary"
    )

    answer = gr.Textbox(
        label="Grounded Answer",
        lines=10
    )

    sources = gr.Textbox(
        label="Sources Retrieved",
        lines=5
    )

    gr.Examples(
        examples=[
            ["Which courses are the hardest?"],
            ["How many hours per week do students spend?"],
            ["What do students say about Advanced Predictive Models?"],
            ["Can students complete the program while working full-time?"],
            ["What is the best dining hall at UT Austin?"]
        ],
        inputs=question
    )

    gr.Markdown("""
---
### RAG Pipeline

Documents → Chunking → Embeddings → ChromaDB → Retrieval → Groq LLM

Built for AI201 Project 1.
""")

    ask_button.click(
        handle_query,
        inputs=question,
        outputs=[answer, sources]
    )

    question.submit(
        handle_query,
        inputs=question,
        outputs=[answer, sources]
    )


demo.launch(css=css)