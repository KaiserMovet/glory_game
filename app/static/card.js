ColorsBG = {
    black: 14, white: 10, red: 10, green: 13, blue: 12
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
        template.firstElementChild.setAttribute('style', `background-image: url(${this.bg_url});`)

        if (can_be_bought) {
            template.firstElementChild.classList.add('buyable')
            template.firstElementChild.setAttribute("onclick", `Game.buyCard('${this.obj_id}')`)
        }
        template.firstElementChild.id = this.obj_id;
        // template.getElementById("color").innerHTML = this.color
        template.getElementById("value").innerHTML = this.value
        template.getElementById("value").classList.add(`card--${this.color}`)
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
                template.getElementById(`cost2_${color}`).setAttribute('style', `width: ${100 - (score * 100 / cost)}%`);

                if (cost > score) template.getElementById(`cost_${color}`).innerHTML = `${score}/${cost}`;
                if (score == 0) template.getElementById(`cost2_${color}`).innerHTML = cost;

                // if (score < cost) {
                //     template.getElementById(`cost_${color}`).innerHTML += ` (${score - cost})`
                // }
            }
        }
        console.log(template)
        return template
    }


}