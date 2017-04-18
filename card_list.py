from flask import json, Flask

cardsHTML = ""

app = Flask(__name__)


@app.route('/')
def list_cards():
    return cardsHTML


def get_cards():
    global cardsHTML
    with open('./cards.json', 'r') as cards:
        card_json = json.load(cards)

        cards = [
            card_json['Basic'],
            card_json['Classic'],
            card_json['Hall of Fame'],  # classic but no longer standard
            card_json['Goblins vs Gnomes'],
            card_json['Naxxramas'],
            card_json['The Grand Tournament'],
            card_json['Blackrock Mountain'],
            card_json['The League of Explorers'],
            card_json['Whispers of the Old Gods'],
            card_json['Karazhan'],
            card_json['Mean Streets of Gadgetzan'],
            card_json['Journey to Un\'Goro'],
        ]

        for set in cards:
            for card in set:
                if card['type'] not in ('Enchantment', 'Hero', 'Hero Power') and \
                                'collectible' in card and card['collectible'] is True:
                    cardsHTML += \
                        '<div style="float:left"><p>' + card['name'] + '</p><img src="' + card['img'] + '" /></div>'


if __name__ == "__main__":
    get_cards()

    app.run(debug=True, port=8000)
