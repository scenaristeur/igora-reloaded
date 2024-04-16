import express from 'express';

const app = express();

app.get("/", (req, res) => {
    res.send("hello");
});


app.post("/v1/chat/completions", express.json(), async (req, res) => {
    console.log("received", req.body);
})

app.listen(3000);