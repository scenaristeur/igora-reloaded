import express from 'express';

const app = express();

app.post("/v1/chat/completions", express.json(), async (req, res) => {
    console.log("received", req.body);
})

//Define request response in root URL (/)
app.get('/', function (req, res) {
    res.send('Hello World')
  })
  
  //Launch listening server on port 8080
  app.listen(5678, function () {
    console.log('App listening on port 5678!')
  })