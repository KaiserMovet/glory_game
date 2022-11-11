

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

    getHTML() {
        var template = this.getTemplate()
        template.firstElementChild.classList.add(`card--${this.color}`);
        template.firstElementChild.id = this.obj_id;
        template.getElementById("color").innerHTML = this.color
        template.getElementById("value").innerHTML = this.value
        for (const [color, cost] of Object.entries(this.cost)) {
            console.log(`cost_${color}`)
            template.getElementById(`cost_${color}`).innerHTML = cost.toString()
        }
        return template
    }
}