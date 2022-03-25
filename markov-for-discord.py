"""A Markov chain generator that can tweet random messages."""

import sys
import os
import discord
from random import choice


client_token = os.environ.get('LAUREL_DISCORD_TOKEN')

########### MARKOV FUNCTIONS ######################
def open_and_read_file(file_path):
    """Take file path as string; return text as string.

    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """
    text_source = open(file_path)
    file_as_string = text_source.read()
    file_as_string = file_as_string.replace("\n", " ")

    return file_as_string

def make_chains(text_string):

    words = text_string.split()
    chains = {}

    for i in range(len(words)):
        if i == 0:
            continue
        
        word1 = words[i-1]
        word2 = words[i]
        if i == len(words) - 1:
            following = None
        else:
            following = words[i+1]

        chains[(word1, word2)] = chains.get((word1, word2), []) + [following]
    
    return chains


def make_text(chains):
    """Return text from chains."""
    
    words = []
    keys_list = list(chains.keys())

    current_key = choice(keys_list)

    while True:
        
        words.append(current_key[0])
        if current_key[0].endswith("."):
            break
        next_word = choice(chains[current_key])
        
        
        if next_word == None:
            words.append(current_key[1])
            break

        new_key = (current_key[1], next_word)
        
        current_key = new_key 
        


    return ' '.join(words)

def markov_text_maker(input_path):
    input_text = open_and_read_file(input_path)
    chains = make_chains(input_text)
    markov_text = make_text(chains)

    return markov_text

################# AVAILABLE INPUT FILES ####################
green_eggs = 'green-eggs.txt'
george = "george_carlin.txt"
jaden = "jaden-tweets.txt"


##########################

client = discord.Client() ##some discord method to create a client

@client.event ##at a specified event
async def on_ready(): ##event is log in
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message): ##event is receiving a message
    if message.author == client.user: ##checks if the client sent the message to itself
        return

    if message.content.startswith('hello'): ##only responds to outside messages
        await message.channel.send('Hello!')
    
    if message.content.startswith('$laurel'): 
        await message.channel.send(markov_text_maker(green_eggs)) #runs the markov maker as input



# client.run(os.environ.get('LAUREL_DISCORD_TOKEN')) 