import "dotenv/config";
import express from "express";
import { ChatCompletionResponse } from "./ChatCompletionResponse/index.js";
// console.log(process.env)
const port = process.env.PORT || 5678;
const llama_port = process.env.LLAMA_CPP_PORT || 8000;

const app = express();

app.post("/v1/chat/completions", express.json(), async (req, res) => {
  console.log("received", req.body);
  let chatCompletionReponse = new ChatCompletionResponse(req.body);
  let llm_url = `http://localhost:${llama_port}/v1/chat/completions`;
  if (req.body.stream == true) {
    res.writeHead(200, {
      "Cache-Control": "no-store",
      "Content-Type": "text/event-stream",
      "Transfer-Encoding": "chunked",
    });

    fetch(llm_url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(req.body),
    })
      .then((response) => {
        // Get the readable stream from the response body
        const stream = response.body;
        // Get the reader from the stream
        const reader = stream.getReader();
        // Define a function to read each chunk
        const readChunk = () => {
          // Read a chunk from the reader
          reader
            .read()
            .then(({ value, done }) => {
              // Check if the stream is done
              if (done) {
                // Log a message
                console.log("Stream finished");
                // res.write('data: [DONE]');
                res.end();
                // Return from the function
                return;
              }
              // Convert the chunk value to a string
              const chunkString = new TextDecoder().decode(value);
              // Log the chunk string
              //console.log(chunkString);
              res.write(chunkString);
              // Read the next chunk
              readChunk();
            })
            .catch((error) => {
              // Log the error
              console.error(error);
            });
        };
        // Start reading the first chunk
        readChunk();
      })
      .catch((error) => {
        // Log the error
        console.error(error);
      });
  } else {
    fetch(llm_url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(req.body),
    })
      .then((llm_reps) => {
        return llm_reps.json();
      })
      .then((llm_reps) => {
        console.log(llm_reps);
        console.log(llm_reps.choices[0].message.content);
        res.json(llm_reps);
      });
  }
});

app.get("/v1/models", (req, res) => {
  let models = {
    object: "list",
    data: [
      {
        id: "./models/dolphin-2.2.1-mistral-7b.Q2_K.gguf",
        object: "model",
        owned_by: "me",
        permissions: [],
      },
    ],
  };
  res.write(JSON.stringify(models));
  res.end();
});

app.get("/", function (req, res) {
  res.sendFile(new URL("./index.html", import.meta.url).pathname);
});

app.get("/health", function (req, res) {
  res.send("ok");
});
//Launch listening server on port 8080
app.listen(port, function () {
  console.log(`App listening on port ${port}!`);
});
