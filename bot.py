import discord
import os
import random
import re
import json
import responses

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Load JSON data
def load_json(file):
    with open(file) as bot_responses:
        print(f"Loaded '{file}' successfully!")
        return json.load(bot_responses)

# Store JSON data
response_data = load_json("resp.json")

@client.event
async def on_ready():
    print(f'{client.user} is now running!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    username = str(message.author)
    user_message = str(message.content)
    channel = str(message.channel)

    print(f'{username} said: "{user_message}" ({channel})')
    
    if user_message.startswith('?'):
        user_message = user_message[1:].strip()
        response = get_response(user_message)
        await send_message(message, response, is_private=True)  # Pass 'response' instead of 'user_message'
    else:
        response = get_response(user_message)
        await send_message(message, response, is_private=False)  # Pass 'response' instead of 'user_message'

async def send_message(message, response, is_private):
    try:
        if is_private:
            await message.author.send(response)
        else:
            await message.channel.send(response)

    except Exception as e:
        print(e)

def get_response(input_string):
    p_message = input_string.lower()  # Use the input_string provided as an argument

    if p_message == 'roll':
        return str(random.randint(1, 6))

    if p_message == '!help':
        return '`To use the chat bot look at the json file to know what to write`'

    split_message = re.split(r'\s+|[,;?!.-]\s*', p_message)  # Moved inside get_response function
    score_list = []

    for response in response_data:
        response_score = 0
        required_score = 0
        required_words = response["required_words"]

        if required_words:
            for word in split_message:
                if word in required_words:
                    required_score += 1

        if required_score == len(required_words):
            for word in split_message:
                if word in response["user_input"]:
                    response_score += 1

        score_list.append(response_score)

    best_response = max(score_list)
    response_index = score_list.index(best_response)

    if input_string == "":
        return "Please type something so we can chat :("

    if best_response != 0:
        return response_data[response_index]["bot_response"]

    return responses.random_string()

my_secret = os.environ['TOKEN']
client.run(my_secret)
