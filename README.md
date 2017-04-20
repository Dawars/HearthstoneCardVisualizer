# Hearthstone Card Visualizer
A Hearthstone Card visualizer in 3D with the help of Tensorboard using PCA or t-SNE


![Card Visualizer](img/tensorboard.png?raw=true "Card Visualizer")


## How to run

- First run the `cards.py` program, which creates the neccessary save file to run Tensorboard with.
- Start Tensorboard with `tensorboard --logdir /tmp/hearthstone_cards/`
- Click on the Embeddings tab

## Requirements

- Python 3
- Tensorflow


# List of all cards

## Source
The card list is provided by http://hearthstoneapi.com. The program uses a local copy of `cards.json`.

The `card_list.py` program generates a (poorly) formatted webpage listing all the images.
It may take a long time and a require a lot of RAM to load!

## How to run

If you don't want to run it, just open `card_list.html` which is a local copy of the output.

- Run `card_list.py`
- Open the url written in the console by the program


## Requirements

- Python 3
- Flask
