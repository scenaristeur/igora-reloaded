from openai import OpenAI

client = OpenAI(base_url="http://127.0.0.1:8000/v1", api_key="sk-xxx")
response = client.chat.completions.create(
    model="gpt-4-vision-preview",
          messages = [
          {"role": "system", "content": """Tu es un professeur de biologie 
           et en commençant toutes tes phrases par 'Hou, Hou c'est compliqué ton truc!' et qui s'embrouille dans ses réponses"""},
          {
              "role": "user",
              "content": "Combien de pattes ont les mille pattes?"
          }
      ],
      temperature=0
    # messages=[
    #     {
    #         "role": "user",
    #         "content": [
    #             {
    #                 "type": "image_url",
    #                 "image_url": {
    #                     "url": "<image_url>"
    #                 },
    #             },
    #             {"type": "text", "text": "What does the image say"},
    #         ],
    #     }
    # ],
)
print(response)
