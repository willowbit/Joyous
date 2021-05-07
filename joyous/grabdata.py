import discord, json, os, yaml
import random as rnd

def addtofile(item, file, key=None):

    thisdir = os.path.dirname(os.path.realpath(__file__))
    possible_locations = [
        f'{thisdir}/{file}',
        f'{thisdir}/../{file}',
        f'{thisdir}/../data/{file}'
    ]

    fname = possible_locations[key]
    print(fname)
    if os.path.isfile(fname) == False:
        with open(fname, 'x') as f:
            f.write(f'- {item}')
            return
    if os.path.isfile(fname):
        with open(fname, 'r') as f:
            itemlist = yaml.safe_load(f)
        itemlist.append(item)
    with open(fname, 'w+') as f:
        yaml.dump(itemlist, f)

    # fname = f'{thisdir}/../data/{file}'
    # if os.path.isfile(fname) == False:
    #     with open(fname, 'x') as f:
    #         f.write(f'- {item}')
    #         return
    # if os.path.isfile(fname) == True:
    #     with open(fname, 'r') as f:
    #         itemlist = yaml.safe_load(f)
    #     itemlist.append(item)
    # with open(fname, 'w+') as f:
    #     yaml.dump(itemlist, f)

def removefromfile(item, file, message, force=False):
    thisdir = os.path.dirname(os.path.realpath(__file__))
    fname = f'{thisdir}/../data/{file}'
    with open(fname, 'r') as f:
        itemlist = yaml.safe_load(f)
    if force == True:
        for joy in itemlist:
            if item in joy:
                itemlist.remove(joy)
                with open(fname, 'w+') as f:
                    yaml.dump(itemlist, f)
                return joy
    if item in itemlist:
        itemlist.remove(item)
    else:
        return False
    with open(fname, 'w+') as f:
        yaml.dump(itemlist, f)

def fetch_file(file):
    thisdir = os.path.dirname(os.path.realpath(__file__))

    possible_locations = [
        f'{thisdir}/{file}',
        f'{thisdir}/../{file}',
        f'{thisdir}/../data/{file}'
    ]

    for fname in possible_locations:
        if os.path.isfile(fname):
            with open(fname, 'r') as f:
                x = yaml.safe_load(f)
                return x
    
    raise Exception(f'File not found: {file}')


msg_blacklist = [
    'faggot', 'fag', 'nigger', 'kill yourself', 'kill urself', 'tranny', 'sweartest', 'Faggot', 'Fag', 'Nigger', 'Tranny'
]