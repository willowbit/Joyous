import discord
import random as rnd
import json


def remove_joy(joy):
    with open('joydata.json', 'r') as f:
        joys = json.load(f)
    
    print(joys)
    joys.remove(joy)

    with open('joydata.json', 'w+') as f:
        json.dump(joys, f)

def addtofile(item, file):
    with open(file, 'r') as f:
        itemlist = json.load(f)
    itemlist.append(item)
    with open(file, 'w+') as f:
        json.dump(itemlist, f)

def fetch_file(file):
    with open(f'{file}', 'r') as f:
        itemlist = json.load(f)
        return itemlist

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

