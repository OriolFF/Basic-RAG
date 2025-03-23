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


    relevantdocs = collection.query(query_embeddings=[queryembed], n_results=5)["documents"][0]
    docs = "\n\n".join(relevantdocs)
    modelquery = f"{query} - Answer that question using the following text as a resource: {docs}"

    stream = ollama.generate(model=mainmodel, prompt=modelquery, stream=True)

    for chunk in stream:
     if chunk["response"]:
        print(chunk['response'], end='', flush=True)