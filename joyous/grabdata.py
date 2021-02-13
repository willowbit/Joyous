import discord, json, os.path, yaml
import random as rnd

def addtofile(item, file):
    thisdir = os.path.dirname(os.path.realpath(__file__))
    fname = f'{thisdir}/../data/{file}'
    if os.path.isfile(fname) == False:
        open(fname, 'x')
        with open(fname, 'w') as f:
            f.write('[]')
    with open(fname, 'r') as f:
        itemlist = yaml.load(f)
    itemlist.append(item)
    with open(fname, 'w+') as f:
        yaml.dump(itemlist, f)

def removefromfile(item, file):
    thisdir = os.path.dirname(os.path.realpath(__file__))
    fname = f'{thisdir}/../data/{file}'
    with open(fname, 'r') as f:
        itemlist = yaml.safe_load(f)
    itemlist.remove(item)
    with open(fname, 'w+') as f:
        yaml.dump(itemlist, f)

def fetch_file(file):
    thisdir = os.path.dirname(os.path.realpath(__file__))
    fname = f'{thisdir}/../data/{file}'
    with open(fname, 'r') as f:
        x = yaml.safe_load(f)
        return x

msg_blacklist = [
    'faggot', 'fag', 'nigger', 'nigga', 'kill yourself', 'kill urself', 'tranny', 'sweartest', 'Faggot', 'Fag', 'Nigger', 'Nigga', 'Tranny'
]