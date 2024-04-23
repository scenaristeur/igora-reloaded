//import express from express
import { ChromaClient } from 'chromadb'
import { HuggingFaceTransformersEmbeddings } from "@langchain/community/embeddings/hf_transformers";

const model = new HuggingFaceTransformersEmbeddings({
    model: "Xenova/all-MiniLM-L6-v2",
  });
  
  /* Embed queries */
  const res = await model.embedQuery(
    "What would be a good company name for a company that makes colorful socks?"
  );
  console.log({ res });
  /* Embed documents */
  const documentRes = await model.embedDocuments(["Hello world", "Bye bye"]);
  console.log({ documentRes });

const client = new ChromaClient();



const collection = await client.getCollection({
    name: "my_collection",
  });

await collection.add({
    ids: ["id1", "id2"],
    metadatas: [{ source: "my_source" }, { source: "my_source" }],
    documents: ["This is a document", "This is another document"],
  });

const results = await collection.query({
    nResults: 2,
    queryTexts: ["This is a query document"],
  });

console.log(results)