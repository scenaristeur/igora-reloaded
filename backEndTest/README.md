
```
python3 -m llama_cpp.server --model ./models/dolphin-2.2.1-mistral-7b.Q2_K.gguf

python3 -m llama_cpp.server --model ./models/llama-pro-8b-instruct.Q2_K.gguf --port 5677
```
```
curl --noproxy '*' -d '{
messages = [
          {"role": "system", "content": """Tu es un professeur de biologie 
           et en commençant toutes tes phrases par Yo !"""},
          {
              "role": "user",
              "content": "Combien de pattes ont les mille pattes?"
          }
      ],
}' -H "Content-Type: application/json" -X POST http://127.0.0.1:8000/v1/chat/completion
```

```
curl --noproxy '*' -X 'POST' \
  'http://localhost:8000/v1/completions' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "prompt": "\n\n### Instructions:\nQuelle est la capitale du Brésil? Si tu ne connais pas, dis que tu ne sais pas et explique pourquoi\n\n### Response:\n",
  "stream": false,
  "stop": [
    "\n",
    "###"
  ]
}'
```