/**
 * Created by dawars on 4/9/17.
 */
var express = require('express');

var app = express();

app.listen(process.env.port | 3000, function () {
    console.log('HS card app listening on port 80!')
});

var cardsJSON = require('./cards.json');

var cards = [
    cardsJSON['Basic'],
    cardsJSON['Classic'],
    cardsJSON['Hall of Fame'], // classic but no longer standard
    cardsJSON['Goblins vs Gnomes'],
    cardsJSON['Naxxramas'],
    cardsJSON['The Grand Tournament'],
    cardsJSON['Blackrock Mountain'],
    cardsJSON['The League of Explorers'],
    cardsJSON['Whispers of the Old Gods'],
    cardsJSON['Karazhan'],
    cardsJSON['Mean Streets of Gadgetzan'],
    cardsJSON['Journey to Un\'Goro']
];

console.log("done parsing");


var processedCards = [];
var cardsHTML = "";

for (var i = 0; i < cards.length; i++) {
    var set = cards[i];
    for (var j = 0; j < set.length; j++) {
        var card = set[j];
        if (
            //card.img !== undefined &&
        // card.type === 'Minion' &&
        card.type !== 'Enchantment' && card.type !== 'Hero' && card.type !== 'Hero Power' &&
        card.collectible !== undefined && card.collectible === true) {
            console.log(card.cardId + "    " + card.name);
            processedCards += card;
            cardsHTML += '<div style="float:left"><p>' + card.name + '</p><img src="' + card.img + '" /></div>';
        }
    }
}

app.get('/', function (req, res) {
    res.setHeader('Content-Type', 'text/html');
    res.write(cardsHTML);
    res.end()

});
