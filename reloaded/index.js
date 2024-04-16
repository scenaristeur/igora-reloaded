import 'dotenv/config'
import express from 'express';
// console.log(process.env)
const port = process.env.PORT || 5678

const app = express();

app.post("/v1/chat/completions", express.json(), async (req, res) => {
    console.log("received", req.body);
})

//Define request response in root URL (/)
app.get('/', function (req, res) {
    // let accueil = `<h1>Igora reloaded</h1>
    // <a href="https://github.com/scenaristeur/igora-reloaded">https://github.com/scenaristeur/igora-reloaded</a>`;
    // res.send(accueil)
    res.sendFile(new URL("./index.html", import.meta.url).pathname);
  })

  app.get('/health', function (req, res) {
    res.send("ok")
  })
  
  //Launch listening server on port 8080
  app.listen(port, function () {
    console.log(`App listening on port ${port}!`)
  })