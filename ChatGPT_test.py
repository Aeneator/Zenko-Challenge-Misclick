import openai

API_KEY = open("API_KEY.txt", 'r').read()
openai.api_key = API_KEY

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "assistant", "content": "What is the general opinion on Katy Perry?"}
    ]
)

print(response)