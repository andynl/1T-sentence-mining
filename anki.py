import urllib.request
import json

url = 'http://localhost:8765'
deck = 'Testing'
model = 'LLNTemplate'

def request(action, **params):
    return {'action': action, 'params': params, 'version': 6}

def invoke(action, **params):
    requestJson = json.dumps(request(action, **params)).encode('utf-8')
    response = json.load(urllib.request.urlopen(urllib.request.Request(url, requestJson)))
    if len(response) != 2:
        raise Exception('response has an unexpected number of fields')
    if 'error' not in response:
        raise Exception('response is missing required error field')
    if 'result' not in response:
        raise Exception('response is missing required result field')
    if response['error'] is not None:
        raise Exception(response['error'])
    return response['result']

# ----------------------------------------------------

def check_matched_word(words):
    print("Check Matched Word")
    anki_data = []
    anki = json.load(open("anki.json", "r"))
    for old in anki:
        anki_data.append(old["fields"]["Lemma"]["value"])

    reactor_data = []
    for new in words:
        reactor_data.append(new["word"])

    return set(reactor_data) ^ set(anki_data)

def anki_conn():
    print("Anki Connection")
    notes = invoke('findCards', query='deck:' + deck)
    result = invoke('cardsInfo', cards=notes)
    with open('anki.json', 'w') as fp:
        json.dump(result, fp)

def anki_store(word, item_key):
    print("Anki Store")
    filename = "{}.png".format(item_key)
    note = {
        "deckName": "English::Language Reactor",
        "modelName": model,
        "fields": {
            "Word Definition": "-",
            "Item Key": item_key,
            "Subtitle": word["sentence"],
            "Word": word["word"],
            "Translation": word["translation"],
            "Video ID": word["video_id"],
            "Video Title": word["video_title"],
            "Date Created": word["date_created"],
            "Lemma": word["word"],
            "Source": word["source"],
            "Next Image Media Filename": filename,
            # "Audio Clip Media filename": ""
        },
        "options": {
            "allowDuplicate": False
        },
        "tags": [
            "green"
        ],
    }
    invoke('addNote', note=note)

def get_new_cards():
    amount = 0
    cards = invoke('findCards', query='deck:' + deck)
    result = invoke("cardsInfo", cards=cards)
    for card in result:
        if card.get('queue') == 0:
            amount += 1
    return amount

def get_learning_cards():
    amount = 0
    cards = invoke('findCards', query='deck:' + deck)
    result = invoke("cardsInfo", cards=cards)
    for card in result:
        if card.get('queue') == 1 or card.get('queue') == 3:
            amount += 1
    return amount

def get_young_cards():
    amount = 0
    cards = invoke('findCards', query='deck:' + deck)
    result = invoke("cardsInfo", cards=cards)
    for card in result:
        if card.get('queue') == 2 and card.get('interval') < 21:
            amount += 1
    return amount

def get_mature_cards():
    amount = 0
    cards = invoke('findCards', query='deck:' + deck)
    result = invoke("cardsInfo", cards=cards)
    for card in result:
        if card.get('queue') == 2 and card.get('interval') >= 21:
            amount += 1
    return amount

def get_suspended_cards():
    amount = 0
    cards = invoke('findCards', query='deck:' + deck)
    result = invoke("cardsInfo", cards=cards)
    for card in result:
        if card.get('queue') == -1:
            amount += 1
    return amount

def get_buried_cards():
    amount = 0
    cards = invoke('findCards', query='deck:' + deck)
    result = invoke("cardsInfo", cards=cards)
    for card in result:
        if card.get('queue') == -2 or card.get('queue') == -3:
            amount += 1
    return amount

def get_erase_cards():
    pass

def today_reps():
    print('Calculating todays reps...')
    cards = invoke('findCards', query='rated:1')
    return len(cards)

def week_reps():
    print('Calculating this weeks reps...')
    cards = invoke('findCards', query='rated:7')
    return len(cards)

def streak():
    streak = 29
    days_ago = 29
    while len(invoke('findCards', query='rated:' + str(days_ago) + ' -rated:' + str(days_ago - 1))) > 0:     # checking if cards were seen days_ago days ago
        days_ago += 1
        streak += 1
        print(days_ago)
    return streak