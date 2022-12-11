ColorsBG = {
    black: 24, white: 21, red: 27, green: 27, blue: 33
}

class Card {
    constructor(card_data) {
        this.obj_id = card_data.obj_id;
        this.color = card_data.color;
        this.value = card_data.value;
        this.cost = card_data.cost;
        this.bg = card_data.bg;
        this.bg_url = ""
        if (this.bg > 0) {
            var bg_index = (this.bg % ColorsBG[this.color]) + 1
            this.bg_url = `${window.location.origin}/static/bg/${this.color}/${bg_index}.png`
        }
    }

    getInvTemplate() {
        return document.getElementById("CardInvTemplate").content.cloneNode(true);
    }
}


class CardElement {
    constructor(card, parent_div) {
        this.card = card;
        this.obj_id = card.obj_id
        this.element_id = `card-${card.obj_id}`;
        this.parent_div = parent_div
        this.parent_div.append(this.getHTML())
        this.element = this.parent_div.querySelector(`#${this.element_id}`)
    }

    getTemplate() {
        return document.getElementById("CardTemplate").content.cloneNode(true);
    }
    // Generate element with all static data
    getHTML() {
        var template = this.getTemplate()
        template.firstElementChild.classList.add(`card--${this.card.color}`);
        template.firstElementChild.setAttribute('style', `background-image: url(${this.card.bg_url});`)
        template.firstElementChild.id = this.element_id;
        template.getElementById("value").innerHTML = this.card.value
        template.getElementById("value").classList.add(`card--${this.card.color}`)
        for (const [color, cost] of Object.entries(this.card.cost)) {
            if (cost == '0') {
                template.getElementById(`cost_${color}`).parentNode.hidden = true
                continue
            }
            template.getElementById(`cost_${color}`).setAttribute('aria-valuemax', cost);
            template.getElementById(`cost_${color}`).innerHTML = cost;

        }
        return template
    }

    update(player = null) {
        var template = this.element
        // If player can buy card, add 'buyable'
        if (player != null && player.canBuyCard(this.card)) {
            template.classList.add('buyable')
            template.setAttribute("onclick", `Game.buyCard('${this.card.obj_id}')`)
        } else {
            template.classList.remove('buyable')
        }

        for (const [color, cost] of Object.entries(this.card.cost)) {
            if (player != null) {
                let score = player.getColorScore(color)

                template.querySelector(`#cost_${color}`).setAttribute('style', `width: ${Math.min(score * 100 / cost, 100)}%`);

                if (cost > score) {
                    template.querySelector(`#cost_${color}`).innerHTML = `${score}/${cost}`;
                    template.querySelector(`#cost2_${color}`).setAttribute('style', `width: ${100 - (score * 100 / cost)}%`);
                }
                if (cost <= score) {
                    template.querySelector(`#cost_${color}`).innerHTML = cost;
                    template.querySelector(`#cost2_${color}`).setAttribute('style', `width:0%`);
                }

                if (score == 0) template.querySelector(`#cost2_${color}`).innerHTML = cost;
                else template.querySelector(`#cost2_${color}`).innerHTML = ""

            }
        }
    }

    delete() {
        this.parent_div.removeChild(this.element);
    }
}

class HiddenCardElement {
    constructor(level, parent_div) {
        this.level = level;
        this.element_id = `hiddencard-${this.level}`;
        this.parent_div = parent_div
        this.parent_div.append(this.getHTML())
        this.element = this.parent_div.querySelector(`#${this.element_id}`)
    }

    getTemplate() {
        return document.getElementById("HiddenCardTemplate").content.cloneNode(true);
    }
    // Generate element with all static data
    getHTML() {
        var template = this.getTemplate()
        // template.firstElementChild.classList.add(`hiddencard-${this.level}`)
        template.firstElementChild.id = this.element_id;
        return template
    }

    update(data) {
        var template = this.element
        console.log(23123)
        let cards_count = data['cards_in_deck'][this.level] - 5
        if (cards_count <= 0) {
            return -1
        }
        template.querySelector("#value").innerHTML = cards_count
        return 0
    }

    delete() {
        this.parent_div.removeChild(this.element);
    }
}