from app.config import client
from app.config import MODEL_NAME

stream = client.chat.completions.create(

    model=MODEL_NAME,

    messages=[
        {
            "role": "user",
            "content": "Explain transformers in 100 words."
        }
    ],

    stream=True

)

for chunk in stream:

    token = chunk.choices[0].delta.content

    if token:

        print(token, end="", flush=True)