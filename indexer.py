import ollama, chromadb
from utilities import readtext, getconfig
from mattsollamatools import chunk_text_by_sentences

collectionname="wallboxrag"

def index_documents(path):
    chroma = chromadb.PersistentClient(path=getconfig()["db_path"])
    collections = chroma.list_collections()
    print(collections)

    if collectionname in collections:
        print('deleting collection')
        chroma.delete_collection(collectionname)
    collection = chroma.get_or_create_collection(name=collectionname, metadata={"hnsw:space": "cosine"})

    embedmodel = getconfig()["embedmodel"]

    documents = readtext(path)
    for filename, text in documents.items():
        print(f"\nProcessing {filename}")
        chunks = chunk_text_by_sentences(source_text=text, sentences_per_chunk=7, overlap=0 )
        for index, chunk in enumerate(chunks):
            embed = ollama.embeddings(model=embedmodel, prompt=chunk)['embedding']
            collection.add([filename+str(index)], [embed], documents=[chunk], metadatas={"source": filename})


def main(path):
    index_documents(path)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main("docs_for_test/")

