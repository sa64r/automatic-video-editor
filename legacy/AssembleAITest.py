import requests
from dotenv import dotenv_values

config = dotenv_values('.env')

#### UPLOAD VIDEO URL TO ASSEMBLY.AI ####
# endpoint = 'https://api.assemblyai.com/v2/transcript'

# json = {
#     "audio_url": "https://youtu.be/gPkmT7UN1bE"
# }

# headers = {
#     "authorization": config["ASSEMBLY_AI_API_KEY"],
#     'Content-Type': 'application/json'
# }

# response = requests.post(endpoint, json=json, headers=headers)
# print(response.json())


#### GET TRANSCRIPTION FROM ASSEMBLY.AI ####

id = "o7o6uy32s0-c24e-4b36-b4fb-d8e1e53099ef"

endpoint = "https://api.assemblyai.com/v2/transcript/" + id
headers = {
    "authorization": config["ASSEMBLY_AI_API_KEY"],
}
response = requests.get(endpoint, headers=headers)
print(response.json())
