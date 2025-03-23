import gradio as gr
import ollama
import chromadb
from utilities import getconfig


# Initialize configuration
collectionname = "wallboxrag"
embedmodel = getconfig()["embedmodel"]
mainmodel = getconfig()["mainmodel"]
chroma = chromadb.PersistentClient(path=getconfig()["db_path"])

def process_query(message, history):
    # Get collection
    collection = chroma.get_or_create_collection(collectionname)
    
    # Get embeddings for the query
    queryembed = ollama.embeddings(model=embedmodel, prompt=message)['embedding']
    
    # Get relevant documents
    relevantdocs = collection.query(query_embeddings=[queryembed], n_results=5)["documents"][0]
    docs = "\n\n".join(relevantdocs)
    
    # Prepare the model query with context
    modelquery = f"{message} - Answer that question using the following text as a resource: {docs}"
    
    # Generate response
    response = ""
    stream = ollama.generate(model=mainmodel, prompt=modelquery, stream=True)
    
    for chunk in stream:
        if chunk["response"]:
            response += chunk["response"]
    
    return response

def chat_interface(message, history):
    # Process the query and get response
    bot_response = process_query(message, history)
    
    # Return the message pair (user message, bot response)
    history.append((message, bot_response))
    return "", history

# Create the Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("# RAG Chat Interface")
    
    chatbot = gr.Chatbot(
        show_label=False,
        height=400
    )
    
    with gr.Row():
        msg = gr.Textbox(
            label="Message",
            placeholder="Ask your question here...",
            show_label=False
        )
        submit = gr.Button("Send")
    
    # Clear button
    clear = gr.Button("Clear")
    
    # Set up event handlers
    submit.click(
        chat_interface,
        inputs=[msg, chatbot],
        outputs=[msg, chatbot],
    )
    msg.submit(
        chat_interface,
        inputs=[msg, chatbot],
        outputs=[msg, chatbot],
    )
    clear.click(lambda: None, None, chatbot, queue=False)

# Launch the app
if __name__ == "__main__":
    demo.launch() 