from openai import OpenAI

# client = OpenAI(api_key="pk-swAmmfqGxOtmoYEnoBtCjNWPBddlTOcQzrGyXEduUwDLGNDl", base_url="https://api.pawan.krd/pai-001-light-rp/v1")
client = OpenAI(api_key="pk-swAmmfqGxOtmoYEnoBtCjNWPBddlTOcQzrGyXEduUwDLGNDl", base_url="http://localhost:4321/v1")

response = client.chat.completions.create(
  model="gpt-4-vision-preview",
  messages=[
    {
      "role": "user",
      "content": [
        {"type": "text", "text": "What’s in this image?"},
        {
          "type": "image_url",
          "image_url": {
            "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg",
          },
        },
      ],
    }
  ],
  max_tokens=300,
)

print(response.choices[0])