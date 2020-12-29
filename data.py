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

questions = [
    'What is something not many people know about you?'
]