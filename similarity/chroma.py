# Install pip install chromadb
import csv
import chromadb



def populate_db():
    with open ('test.csv') as file:
        lines = csv.reader(file)

        documents_csv = []
        metadata_csv = []
        ids_csv =[]

        for i, line in enumerate(lines):
            documents_csv.append(line[1])
            metadata_csv.append({"source": line[0]})
            ids_csv.append(str(i))
    
    return [documents_csv, metadata_csv, ids_csv]


def main ():

    nb_result = 5

    with open ('test.csv') as file:
        lines = csv.reader(file)

        documents_csv = []
        metadata_csv = []
        ids_csv =[]

        for i, line in enumerate(lines):
            documents_csv.append(line[1])
            metadata_csv.append({"source": line[0]})
            ids_csv.append(str(i))

    # setup Chroma in-memory, for easy prototyping. Can add persistence easily!
    chroma_client = chromadb.Client()

    # Create collection. get_collection, get_or_create_collection, delete_collection also available!
    collection = chroma_client.create_collection("my-collection")

    # collection = chroma_client.create_collection(name="my_collection")
    collection.add(
        documents=documents_csv,
        metadatas=metadata_csv,
        ids=ids_csv
    )

    results = collection.query(
        query_texts=["produits de la mer"],
        n_results=nb_result
    )
    for i in range(nb_result):
        print(f'id:{results["ids"][0][i]}, distance:{results["distances"][0][i]}, source: {results["metadatas"][0][i]["source"]}, message: {results["documents"][0][i]}')
    #print(results)

if __name__ == "__main__":
    main()
