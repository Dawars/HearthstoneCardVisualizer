import os
from operator import itemgetter
from shutil import copyfile

import json
import tensorflow as tf
from collections import defaultdict

LOGDIR = '/tmp/hearthstone_cards/'
METADATA_FILE = 'labels.tsv'

card_features = [
    # cost, attack, health, durability,type, battlecry, deathrattle, spelldamage, stealth, taunt, charge, race,
]

valid_sets = [
    'Basic',
    'Classic',
    'Hall of Fame',  # classic but no longer standard
    'Goblins vs Gnomes',
    'Naxxramas',
    'The Grand Tournament',
    'Blackrock Mountain',
    'The League of Explorers',
    'Whispers of the Old Gods',
    'Karazhan',
    'Mean Streets of Gadgetzan',
    'Journey to Un\'Goro'
]


def check_value(card, param, default=None):
    if param in card:
        return card[param]
    else:
        return default


def has_mechanics(card, mechanic):
    mech_list = check_value(card, 'mechanics', [])

    for mech in mech_list:
        if mech['name'] == mechanic:
            return True
    return False


def gen_metadata():
    """
    Generate metadata and populate feature list
    """
    cards = []
    with open('./cards.json') as json_data:  # load json from HearthstoneAPI
        d = json.load(json_data)
        for set_name in d:
            if set_name in valid_sets:  # remove debug cards
                for card in d[set_name]:
                    # remove non collectible cards
                    if card['type'] != 'Enchantment' and card['type'] != 'Hero' and card['type'] != 'Hero Power' and \
                                    'collectible' in card and card['collectible'] is True:
                        cards.append(card)

    # sort to match spritesheet order
    cards_sorted = sorted(cards, key=itemgetter('cardId'))

    # write tsv file
    with open(os.path.join(LOGDIR, METADATA_FILE), 'w') as file:
        file.write('Name\tId\tType\tMana cost\tAttack\tHealth\tDurability\tBattlecry\tDeathrattle\tSpelldamage\tStealth'
                   '\tTaunt\tCharge\tAdapt\tWindfury\tOverload\tInspire\tSilence\tDivine Shield\tFreeze\tPoisonous'
                   '\tDiscover\tCan\'t be targeted\tDiscard\tJade\tC\'Thun\tDraw\tSummon\tDeal damage'
                   '\tCombo\tRace\tSecret\tRarity\tClass\tCard set\tText\n')
        # TODO: Handbuff, more info to spells
        for card in cards_sorted:
            type_list = defaultdict(lambda: -1, dict(Minion=0, Spell=1, Weapon=2))
            race_list = defaultdict(lambda: -1, dict(Beast=0, Dragon=1, Pirate=2, Totem=3, Demon=4, Elemental=5,
                                                     Mech=6, Murlock=7))
            card_features.append([type_list[(check_value(card, 'cost'))],
                                  check_value(card, 'cost', 0),
                                  check_value(card, 'attack', 0),
                                  check_value(card, 'health', 0),
                                  check_value(card, 'durability', 0),
                                  1 if has_mechanics(card, 'Battlecry') else 0,
                                  1 if has_mechanics(card, 'Deathrattle') else 0,
                                  1 if has_mechanics(card, 'Spell Damage') else 0,
                                  1 if has_mechanics(card, 'Stealth') else 0,
                                  1 if has_mechanics(card, 'Taunt') else 0,
                                  1 if has_mechanics(card, 'Charge') else 0,
                                  1 if has_mechanics(card, 'Adapt') else 0,
                                  1 if has_mechanics(card, 'Windfury') else 0,
                                  1 if has_mechanics(card, 'Overload') else 0,
                                  1 if has_mechanics(card, 'Inspire') else 0,
                                  1 if has_mechanics(card, 'Silence') else 0,
                                  1 if has_mechanics(card, 'Divine Shield') else 0,
                                  1 if has_mechanics(card, 'Freeze') else 0,
                                  1 if has_mechanics(card, 'Poisonous') else 0,
                                  1 if has_mechanics(card, 'Discover') else 0,
                                  1 if 'can\'t be targeted by spells or hero powers'
                                       in check_value(card, 'text', "").lower() else 0,
                                  1 if 'discard' in check_value(card, 'text', "").lower() else 0,
                                  1 if 'jade golem' in check_value(card, 'text', "").lower() else 0,
                                  1 if 'c\'thun' in check_value(card, 'text', "").lower() else 0,
                                  1 if 'draw' in check_value(card, 'text', "").lower() else 0,
                                  1 if 'summon' in check_value(card, 'text', "").lower() else 0,
                                  1 if 'deal' in check_value(card, 'text', "").lower() else 0,
                                  1 if has_mechanics(card, 'Combo') else 0,
                                  race_list[check_value(card, 'race')],
                                  1 if has_mechanics(card, 'Secret') else 0,
                                  ])

            # write labels to file
            file.write(
                "{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\t{9}\t{10}\t{11}\t{12}\t{13}\t{14}\t{15}\t{16}\t{17}\t{18}"
                "\t{19}\t{20}\t{21}\t{22}\t{23}\t{24}\t{25}\t{26}\t{27}\t{28}\t{29}\t{30}\t{31}\t{32}\t{33}\t{34}\t{35}"
                "\n"
                    .format(check_value(card, 'name'),
                            check_value(card, 'cardId'),
                            check_value(card, 'type'),
                            check_value(card, 'cost'),
                            check_value(card, 'attack'),
                            check_value(card, 'health'),
                            check_value(card, 'durability'),
                            has_mechanics(card, 'Battlecry'),
                            has_mechanics(card, 'Deathrattle'),
                            has_mechanics(card, 'Spell Damage'),
                            has_mechanics(card, 'Stealth'),
                            has_mechanics(card, 'Taunt'),
                            has_mechanics(card, 'Charge'),
                            has_mechanics(card, 'Adapt'),
                            has_mechanics(card, 'Windfury'),
                            has_mechanics(card, 'Overload'),
                            has_mechanics(card, 'Inspire'),
                            has_mechanics(card, 'Silence'),
                            has_mechanics(card, 'Divine Shield'),
                            has_mechanics(card, 'Freeze'),
                            has_mechanics(card, 'Poisonous'),
                            has_mechanics(card, 'Discover'),
                            'can\'t be targeted by spells or hero powers' in check_value(card, 'text', "").lower(),
                            'discard' in check_value(card, 'text', "").lower(),
                            'jade golem' in check_value(card, 'text', "").lower(),
                            'c\'thun' in check_value(card, 'text', "").lower(),
                            "draw" in check_value(card, 'text', "").lower(),
                            'summon' in check_value(card, 'text', "").lower(),
                            'deal' in check_value(card, 'text', "").lower(),  # todo parse damage value
                            has_mechanics(card, 'Combo'),
                            check_value(card, 'race'),
                            has_mechanics(card, 'Secret'),
                            check_value(card, 'rarity'),
                            check_value(card, 'playerClass'),
                            check_value(card, 'cardSet'),
                            check_value(card, 'text'),
                            ))


def main():
    os.makedirs(os.path.dirname(LOGDIR), exist_ok=True)
    copyfile('./spritesheet.png', os.path.join(LOGDIR, "spritesheet.png"))
    # create metadata tsv file
    gen_metadata()

    sess = tf.Session()

    card_embedding = tf.Variable(tf.zeros([len(card_features), len(card_features[0])]), name="test_embedding")
    assignment = card_embedding.assign(card_features)

    saver = tf.train.Saver()

    sess.run(tf.global_variables_initializer())
    writer = tf.summary.FileWriter(LOGDIR)  # rewrite prev
    writer.add_graph(sess.graph)

    config = tf.contrib.tensorboard.plugins.projector.ProjectorConfig()
    embedding_config = config.embeddings.add()
    embedding_config.tensor_name = card_embedding.name
    embedding_config.sprite.image_path = LOGDIR + 'spritesheet.png'
    embedding_config.metadata_path = LOGDIR + METADATA_FILE
    # Specify the width and height of a single thumbnail.
    embedding_config.sprite.single_image_dim.extend([100, 151])

    tf.contrib.tensorboard.plugins.projector.visualize_embeddings(writer, config)

    sess.run(assignment)
    saver.save(sess, os.path.join(LOGDIR, "model.ckpt"))


if __name__ == '__main__':
    main()
