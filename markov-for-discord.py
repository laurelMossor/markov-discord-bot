"""A Markov chain generator that can tweet random messages."""

import sys
import os
import discord
from random import choice



client_token = os.environ.get('LAUREL_DISCORD_TOKEN')



def open_and_read_file(filenames):
    """Take list of files. Open them, read them, and return one long string."""

    body = ''
    for filename in filenames:
        text_file = open(filename)
        body = body + text_file.read()
        text_file.close()

    return body


def make_chains(text_string):
    """Take input text as string; return dictionary of Markov chains."""

    chains = {}

    words = text_string.split()
    for i in range(len(words) - 2):
        key = (words[i], words[i + 1])
        value = words[i + 2]

        if key not in chains:
            chains[key] = []

        chains[key].append(value)

    return chains


def make_text(chains):
    """Take dictionary of Markov chains; return random text."""

    keys = list(chains.keys())
    key = choice(keys)

    words = [key[0], key[1]]
    while key in chains:
        # Keep looping until we have a key that isn't in the chains
        # (which would mean it was the end of our original text).

        # Note that for long texts (like a full book), this might mean
        # it would run for a very long time.

        word = choice(chains[key])
        words.append(word)
        key = (key[1], word)

    return ' '.join(words)


# Get the filenames from the user through a command line prompt, ex:
# python markov.py green-eggs.txt shakespeare.txt
filenames = sys.argv[1:]

# Open the files and turn them into one long string
text = open_and_read_file(filenames)

# Get a Markov chain
chains = make_chains(text)


client = discord.Client() ##some discord method to create a client

@client.event ##at a specified event
async def on_ready(): ##event is log in
    print('We have logged in as {0.user}'.format(client))##

@client.event
async def on_message(message): ##event is receiving a message
    if message.author == client.user: ##checks if the client sent the message to itself
        return

    if message.content.startswith('$hello'):##only responds to outside messages
        await message.channel.send('Hello!')

client.run(os.environ.get('LAUREL_DISCORD_TOKEN')) ##defines the client with a specific token