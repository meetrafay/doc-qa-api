import gradio as gr
import requests

API_URL = "http://localhost:8000"  # Update if deployed remotely

# Upload text document
def upload_text_doc(title, content):
    response = requests.post(f"{API_URL}/documents", json={
        "title": title,
        "content": content
    })
    return response.json()

# Upload PDF files
def upload_pdf_files(files):
    files_data = [("files", (f.name, open(f.name, "rb"), "application/pdf")) for f in files]
    response = requests.post(f"{API_URL}/documents/pdf-batch", files=files_data)
    return response.json()

# List documents
def list_documents():
    response = requests.get(f"{API_URL}/documents")
    return response.json()

# Query documents
def ask_question(question, top_k):
    response = requests.post(f"{API_URL}/query", json={
        "question": question,
        "top_k": top_k
    })
    return response.json()

# Delete document
def delete_document(doc_id):
    response = requests.delete(f"{API_URL}/documents/" + doc_id)
    return response.json()

# Gradio UI
with gr.Blocks(title="🧠 Resume Q&A System") as demo:
    gr.Markdown("## 📄 Document Q&A with FastAPI + FAISS")

    with gr.Tab("Upload Text"):
        title = gr.Textbox(label="Title")
        content = gr.Textbox(lines=10, label="Content")
        btn_upload_text = gr.Button("Upload Text Doc")
        text_result = gr.JSON(label="Response")
        btn_upload_text.click(upload_text_doc, inputs=[title, content], outputs=text_result)

    with gr.Tab("Upload PDF(s)"):
        pdf_files = gr.File(file_types=[".pdf"], file_count="multiple", label="Upload PDF Files")
        btn_upload_pdf = gr.Button("Upload PDFs")
        pdf_result = gr.JSON(label="Response")
        btn_upload_pdf.click(upload_pdf_files, inputs=[pdf_files], outputs=pdf_result)

    with gr.Tab("List Documents"):
        btn_list = gr.Button("Get Documents")
        doc_list = gr.JSON(label="All Indexed Documents")
        btn_list.click(list_documents, outputs=doc_list)

    with gr.Tab("Ask a Question"):
        question = gr.Textbox(label="Your Question")
        top_k = gr.Slider(1, 10, value=3, step=1, label="Top K Chunks")
        btn_ask = gr.Button("Ask")
        result = gr.JSON(label="Answer & Sources")
        btn_ask.click(ask_question, inputs=[question, top_k], outputs=result)

    with gr.Tab("Delete Document"):
        doc_id = gr.Textbox(label="Document ID to Delete")
        btn_delete = gr.Button("Delete")
        delete_result = gr.JSON(label="Delete Response")
        btn_delete.click(delete_document, inputs=doc_id, outputs=delete_result)

demo.launch()
