

class Card {
    constructor(card_data) {
        this.obj_id = card_data.obj_id;
        this.color = card_data.color;
        this.value = card_data.value;
        this.cost = card_data.cost;
    }

    getTemplate() {
        return document.getElementById("CardTemplate").content.cloneNode(true);
    }
    getInvTemplate() {
        return document.getElementById("CardInvTemplate").content.cloneNode(true);
    }

    getHTML(player = null) {
        let can_be_bought = Game.getCurrentPlayer().canBuyCard(this)
        var template = this.getTemplate()
        template.firstElementChild.classList.add(`card--${this.color}`);

        if (can_be_bought) {
            template.firstElementChild.classList.add('buyable')
            template.firstElementChild.setAttribute("onclick", `Game.buyCard('${this.obj_id}')`)
        }
        template.firstElementChild.id = this.obj_id;
        // template.getElementById("color").innerHTML = this.color
        template.getElementById("value").innerHTML = this.value
        for (const [color, cost] of Object.entries(this.cost)) {
            // template.getElementById(`cost_${color}`).innerHTML = cost.toString()
            if (cost == '0') {
                template.getElementById(`cost_${color}`).parentNode.hidden = true
                continue
            }
            template.getElementById(`cost_${color}`).setAttribute('aria-valuemax', cost);
            template.getElementById(`cost_${color}`).innerHTML = cost;

            if (player != null) {
                let score = player.getColorScore(color)
                template.getElementById(`cost_${color}`).setAttribute('aria-valuenow', score);
                template.getElementById(`cost_${color}`).setAttribute('style', `width: ${score * 100 / cost}%`);
                if (cost > score) template.getElementById(`cost_${color}`).innerHTML = `${score}/${cost}`;


                // if (score < cost) {
                //     template.getElementById(`cost_${color}`).innerHTML += ` (${score - cost})`
                // }
            }
        }
        console.log(template)
        return template
    }


}