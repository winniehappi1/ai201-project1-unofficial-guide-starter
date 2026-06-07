import gradio as gr
from query import ask


def handle_query(question):
    result = ask(question)

    sources = "\n".join(f"- {source}" for source in result["sources"])

    return result["answer"], sources


with gr.Blocks() as demo:
    gr.Markdown("# UT Austin MSDS Unofficial Guide")

    question = gr.Textbox(label="Ask a question")
    button = gr.Button("Ask")

    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Retrieved from", lines=4)

    button.click(handle_query, inputs=question, outputs=[answer, sources])
    question.submit(handle_query, inputs=question, outputs=[answer, sources])

demo.launch()