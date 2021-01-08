import discord
import random as rnd
import json


def add_joy(joy):
###dump the joy
    with open('joydata.json', 'r') as f:
        joys = json.load(f)
    joys.append(joy)
    with open('joydata.json', 'w+') as f:
        json.dump(joys, f)

def fetch_joys():
    with open('joydata.json', 'r') as f:
        joys = json.load(f)
        return joys

def remove_joy(joy):
    with open('joydata.json', 'r') as f:
        joys = json.load(f)
    
    print(joys)
    joys.remove(joy)

    with open('joydata.json', 'w+') as f:
        json.dump(joys, f)

def add_song(joy):
    with open('playlist.json', 'r') as f:
        playlist = json.load(f)
    playlist.append(joy)
    with open('playlist.json', 'w+') as f:
        json.dump(playlist, f)

def fetch_song():
    with open('playlist.json', 'r') as f:
        playlist = json.load(f)
        return playlist

class question:
    def __init__(self, question, example):
        self.question = question
        self.example = example

questions = [
    question("Something most people don't know about me is.....", "Something most people don't know about me is that I love being a bot!! :D."),
    question("Something I accomplished today was......", "Something I accomplished today was finishing all my homework!")
]


def roll():
    qst = rnd.choice(questions)
    qstq = qst.question
    qstex = qst.example

