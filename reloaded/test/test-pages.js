import * as chai from "chai";
import { expect } from "chai";
import chaiHttp from "chai-http";
chai.use(chaiHttp);

let temperature = 12;
let messages = [
  //   { role: "system", content: `répond juste 'Salut'` },
  {
    role: "user",
    content: "Bonjour!",
  },
];

describe("Igora Reloaded API", () => {
  console.log("LE TEST FONCTIONNE AVEC llama-pro-8b-instruct.Q2_K.gguf");
  describe("GET health & models", () => {
    it("page health", (done) => {
      fetch("http://localhost:5678/health")
        .then((res) => {
          return res.text();
        })
        .then((res) => {
          expect(res).to.equal("ok");
          done();
        });
    });

    it("models", (done) => {
      fetch("http://localhost:5678/v1/models")
        .then((res) => {
          return res.json();
        })
        .then((res) => {
          // console.log(res)
          expect(res.data[0].id).to.equal(
            "./models/dolphin-2.2.1-mistral-7b.Q2_K.gguf"
          );
          done();
        });
    });
  }),
    describe("COMPLETIONS", () => {
      // this.timeout(10000);
      it("completion", (done) => {
        //this.timeout(500);
        // setTimeout( 300);
        const body = {
          messages: messages,
          seed: 123,
          stream: false,
        };

        fetch("http://localhost:5678/v1/chat/completions", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(body),
        })
          .then((res) => {
            // console.log(res);
            return res.json();
          })
          .then((res) => {
            // console.log(res);
            let content = res.choices[0].message.content.trim();
            //console.log(content);
            expect(content).to.be.a("string");
            expect(content).to.equal("Salut! Comment allez-vous?");
            done();
          });
      }).timeout(10000);

      it("completion stream", (fini) => {
        let result = "";
        const body = {
          messages: messages,
          seed: 123,
          stream: true,
        };
        fetch("http://localhost:5678/v1/chat/completions", { 
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(body)
            })
            .then(response => {
                // Get the readable stream from the response body
                const stream = response.body;
                // Get the reader from the stream
                const reader = stream.getReader();
                // Define a function to read each chunk
                const readChunk = () => {
                    // Read a chunk from the reader
                    reader.read()
                        .then(({
                            value,
                            done
                        }) => {
                            // Check if the stream is done
                            if (done) {
                                // Log a message
                                //console.log('Stream finished');
                                result = result.trim()
                                //console.log(result);
                                expect(result).to.be.a("string");
                                expect(result).to.equal("Salut! Comment allez-vous?");
                                fini()
                                return;
                            }
                            // Convert the chunk value to a string
                            const chunkString = new TextDecoder().decode(value);
                            // Log the chunk string
                           // console.log(chunkString);
                            // res.write(chunkString);
                            const lines = chunkString.split("\n");
                            const parsedLines = lines
                              .map((line) => line.replace(/^data: /, "").trim())
                              .filter((line) => line != "" && line !== "[DONE]")
                              .map((line) => JSON.parse(line));
              
                            for (const parsedLine of parsedLines) {
                              const { choices } = parsedLine;
                              const { delta } = choices[0];
                              const { content } = delta;
                              if (content && content != "{}") {
                                //console.log(content)
                                // ligne.innerHTML += content;
                                result += content;
                              }
                            }
                             // Read the next chunk
                            readChunk();
                        })
                        .catch(error => {
                            // Log the error
                            console.error(error);
                        });
                };
                // Start reading the first chunk
                readChunk();

     
            })
            .catch(error => {
                // Log the error
                console.error(error);
            });
      }).timeout(10000);
    });
});
