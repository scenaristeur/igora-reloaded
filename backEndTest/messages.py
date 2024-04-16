from llama_cpp import Llama
llm = Llama(
      model_path="models/dolphin-2.2.1-mistral-7b.Q2_K.gguf",
      chat_format="llama-2"
)
output = llm.create_chat_completion(
      messages = [
          {"role": "system", "content": """Tu es un professeur de mathématiques qui expose toutes
           tes réponses avec beaucoup de détails, 
           et en commençant toutes tes phrases par 'Hey, hey bonne question!'"""},
          {
              "role": "user",
              "content": "Combien de pattes ont les araignées?"
          }
      ],
      temperature=0
)
print(output)