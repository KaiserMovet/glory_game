
class Player {
    constructor(name, data) {
        this.name = name;
        this.cards = [];
        for (const [card_id, card_data] of Object.entries(data['cards'])) {
            this.cards.push(new Card(card_data))
        }
        this.coins = data['coins']
    }

    getColorScore(color_name) {
        var score = 0;
        score += this.getColorCardScore()
        score += this.coins[color_name]
        return score
    }

    getColorCardScore(color_name) {
        return this.cards.filter(card => card.color == color_name).length
    }

    getTotalScore() {
        var score = 0;
        for (let card of this.cards.filter(card => card.value >= 1)) score += card.value
        return score
    }


    canBuyCard(card) {
        for (const [color, cost] of Object.entries(card.cost)) {
            if (this.getColorScore(color) < cost) return false
        }
        return true
    }
}