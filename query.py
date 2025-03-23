import ollama, sys, chromadb
from utilities import getconfig

collectionname="wallboxrag"
embedmodel = getconfig()["embedmodel"]
mainmodel = getconfig()["mainmodel"]
chroma = chromadb.PersistentClient(path=getconfig()["db_path"])

def query():
    collection = chroma.get_or_create_collection(collectionname)
    
    query = " ".join(sys.argv[1:])
    
    queryembed = ollama.embeddings(model=embedmodel, prompt=query)['embedding']
    
    # Get results including metadatas
    results = collection.query(
        query_embeddings=[queryembed],
        n_results=5,
        include=['metadatas', 'documents']
    )
    print(f"Found {len(results['documents'][0])} relevant documents")
    
    # Print source documents and their content
    print("\nRelevant documents found in:")
    related_documents=results['metadatas'][0]
    for metadata in related_documents:
        print(f"\nSource: {metadata['source']}")
      
    relevantdocs = results["documents"][0]
    if not relevantdocs:
        print("No relevant documents found!")
        return
        
    docs = "\n\n".join(relevantdocs)
    modelquery = f"{query} - Answer that question using the following text as a resource: {docs}. At the end show a list with a link to source documents:{related_documents}"

    print("\nGenerating answer...\n")
    stream = ollama.generate(model=mainmodel, prompt=modelquery, stream=True)

    for chunk in stream:
        if chunk["response"]:
            print(chunk['response'], end='', flush=True)

if __name__ == "__main__":
    query()