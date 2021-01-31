import discord, json, os.path
import random as rnd

def addtofile(item, file):
    thisdir = os.path.dirname(os.path.realpath(__file__))
    fname = f'{thisdir}/../data/{file}'
    if os.path.isfile(fname) == False:
        open(fname, 'x')
        with open(fname, 'w') as f:
            f.write('[]')
    with open(fname, 'r') as f:
        itemlist = json.load(f)
    itemlist.append(item)
    with open(fname, 'w+') as f:
        json.dump(itemlist, f)

def removefromfile(item, file):
    thisdir = os.path.dirname(os.path.realpath(__file__))
    fname = f'{thisdir}/../data/{file}'
    with open(fname, 'r') as f:
        itemlist = json.load(f)
    itemlist.remove(item)
    with open(fname, 'w+') as f:
        json.dump(itemlist, f)

def fetch_file(file):
    thisdir = os.path.dirname(os.path.realpath(__file__))
    fname = f'{thisdir}/../data/{file}'
    with open(fname, 'r') as f:
        itemlist = json.load(f)
        return itemlist

msg_blacklist = [
    'faggot', 'fag', 'nigger', 'nigga', 'kill yourself', 'kill urself', 'tranny', 'sweartest', 'Faggot', 'Fag', 'Nigger', 'Nigga', 'Tranny'
]