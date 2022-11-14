class Game {

    static data = null

    static getPlayerName() {
        let player_name = window.location.pathname.split('/')[2];
        return player_name
    }

    static checkIfCurrentPlayer() {
        console.log('Checking if current player', this.getPlayerName() == this.data['current_player'])
        return this.getPlayerName() == this.data['current_player'];
    }

    static getCurrentPlayer() {
        return this.data['players'][this.getPlayerName()];
    }



    static buyCard(card_id) {
        if (!this.checkIfCurrentPlayer) return false
        var move = {}
        move['type'] = 'buy'
        move['card_id'] = card_id

        RequestManager.postData(
            aUrl = `/api/player/${Game.getPlayerName()}/move`,
            aCallback = null,
            body = { 'move': move },
        );
        Inter.get_data()

    }

    static disableCoinsToGet(color) {
        if (color == 'all') {
            for (let c_color of ['black', 'blue', 'green', 'red', 'white']) {
                document.getElementById(`deck_chips_${c_color}`).classList.add('deck_chips_disable')
            }
            return
        }
        document.getElementById(`deck_chips_${color}`).classList.add('deck_chips_disable')
    }

    static enableCoinsToGet() {
        for (let c_color of ['black', 'blue', 'green', 'red', 'white']) {
            document.getElementById(`deck_chips_${c_color}`).classList.remove('deck_chips_disable')
        }
    }

    static refresh() {
        document.getElementById('deck_chips_buy').innerHTML = "";
        document.getElementById('deck_chips_buy_button').disabled = true;
        Inter.get_data()
        Game.enableCoinsToGet()
    }

    static getChips() {
        if (!this.checkIfCurrentPlayer()) return
        var busket = document.getElementById('deck_chips_buy')
        var current_colors = []
        for (let current_chip of busket.childNodes) {
            current_colors.push(current_chip.getAttribute('coin_color'))
        }
        var move = {}
        if (current_colors.length == 2 && current_colors[0] == current_colors[1]) {
            // If 2 chips with same color, disable all
            move['type'] = 'get2'
            move['color'] = current_colors[0]
            RequestManager.postData(
                aUrl = `/api/player/${Game.getPlayerName()}/move`,
                aCallback = Game.refresh,
                body = { 'move': move },
            );
        } else {
            // If 3 chips with diffrent color
            move['type'] = 'get3'
            move['colors'] = current_colors
            RequestManager.postData(
                aUrl = `/api/player/${Game.getPlayerName()}/move`,
                aCallback = Game.refresh,
                body = { 'move': move },
            );
        }

    }

    static analyzeBusket() {
        var busket = document.getElementById('deck_chips_buy')
        var current_colors = []

        for (let current_chip of busket.childNodes) {
            current_colors.push(current_chip.getAttribute('coin_color'))
        }

        // If more than one chip, enable buy button
        if (current_colors.length >= 1) {
            document.getElementById('deck_chips_buy_button').disabled = false
        }

        // If only one chip, return
        if (current_colors.length == 1) return

        // If 3 chips or more, disable all
        if (current_colors.length >= 3) {
            this.disableCoinsToGet('all')
            return
        }

        // If 2 chips with same color, disable all
        if (current_colors.length == 2 && current_colors[0] == current_colors[1]) {
            this.disableCoinsToGet('all')
            return
        }

        // If 2 or more chips with diffrent colors,
        // disable only colors, which are already in busket
        for (let c_color of current_colors) {
            this.disableCoinsToGet(c_color)
        }
    }

    static addChipToBusket(color) {
        if (!this.checkIfCurrentPlayer()) return
        Inter.stop_get_data()
        var deck = document.getElementById(`deck_chips_${color}`)
        // If deck has class deck_chips_disable, ignore
        if (deck.classList.contains('deck_chips_disable')) return

        var chip = document.getElementById(`deck_chips_${color}`).lastElementChild
        if (chip == null) return

        var busket = document.getElementById('deck_chips_buy')


        chip.innerHTML = 1
        var current_amount = busket.children.length
        chip.setAttribute('style', `top: ${current_amount * 6 * 3}pt;`)
        chip.classList.remove(`chip-mess`)
        busket.appendChild(chip)
        this.analyzeBusket()


    }
}




function preprareData(data) {
    data = data['response']
    // Prepare Card Objects
    for (const [level, cards] of Object.entries(data['deck'])) {
        new_cards = []
        for (var card of cards) {
            new_cards.push(new Card(card))
        }
        data['deck'][level] = new_cards
    }

    // Prepare Players
    var new_players = {}
    for (const [player_name, player_data] of Object.entries(data['players'])) {
        new_players[player_name] = new Player(player_name, player_data)
    }
    data['players'] = new_players
    return data

}
class Deck {

    static getChips(color, start, end) {
        var chips = []
        for (let i = start; i < end; i++) {
            var chip = document.getElementById("ChipTemplate").content.cloneNode(true);
            chip.firstElementChild.classList.add(`chip--${color}`)
            chip.firstElementChild.classList.add(`chip-mess`)

            chip.firstElementChild.innerHTML = i + 1
            // chip.firstElementChild.setAttribute('style', `top: ${i * 6}pt;`)
            chip.firstElementChild.setAttribute('coin_color', color)

            chips.push(chip)
        }
        return chips
    }

    static renderDeck(data) {
        for (let level of ['1', '2', '3']) {
            let cards = data['deck'][level]
            let deck_div = document.getElementById(`level${level}`)

            // Id of cards, that will be inserted into deck
            let next_id_list = []
            for (let card of cards) {
                next_id_list.push(card.obj_id)
            }
            // Id of cards currently in deck
            // Remove cards, if need to
            let current_id_list = []
            let child_to_remove = []
            for (let child of deck_div.children) {
                if (!next_id_list.includes(child.id)) {
                    child_to_remove.push(child)
                } else {
                    current_id_list.push(child.id)
                }
            }
            for (let child of child_to_remove) {
                deck_div.removeChild(child)
            }

            // Add cards to deck
            for (let card of cards) {

                var new_child = card.getHTML(Game.getCurrentPlayer())

                if (current_id_list.includes(card.obj_id)) {
                    deck_div.replaceChild(new_child, document.getElementById(card.obj_id))
                } else {
                    deck_div.append(new_child)
                }
            }
        }
    }

    static renderChips(coins_data) {
        for (const [color, amount] of Object.entries(coins_data)) {
            var coins = document.getElementById(`deck_chips_${color}`)
            var current_amount = coins.childElementCount
            if (current_amount < amount) {
                for (let chip of this.getChips(color, current_amount, amount)) {
                    coins.appendChild(chip)
                }
            }
            if (current_amount > amount) {
                // child_to_remove = coins.childred.slice(-(current_amount - amount))
                for (let i = 0; i < current_amount - amount; i++) {
                    coins.removeChild(coins.children[amount])
                }

            }
        }
    }

    static render(data) {
        this.renderDeck(data)
        this.renderChips(data['coins'])
    }
}

class MainPlayerDeck {

    static getInventory() {
        return document.getElementById("inventory")
    }

    static getChips(color, start, end) {
        var chips = []
        for (let i = start; i < end; i++) {
            var chip = document.getElementById("ChipTemplate").content.cloneNode(true);
            chip.firstElementChild.classList.add(`chip--${color}`)
            chip.firstElementChild.innerHTML = i + 1
            chip.firstElementChild.setAttribute('style', `left: ${i * 6}pt;`)
            chips.push(chip)
        }
        return chips
    }

    static renderChips(coins_data) {
        for (const [color, amount] of Object.entries(coins_data)) {
            var coins = document.getElementById(`main_player_chip_${color}`)
            var current_amount = coins.childElementCount
            if (current_amount < amount) {
                for (let chip of this.getChips(color, current_amount, amount)) {
                    coins.appendChild(chip)
                }
            }
            if (current_amount > amount) {
                // child_to_remove = coins.childred.slice(-(current_amount - amount))
                for (let i = 0; i < current_amount - amount; i++) {
                    coins.removeChild(coins.children[amount])
                }

            }
        }
    }

    static getColorCard(color) {
        return document.getElementById(`cards_${color}`)
    }

    static renderCards(cards) {
        for (let color of ['black', 'blue', 'green', 'red', 'white']) {
            let card_el = this.getColorCard(color)
            let amount = cards.filter(card => card.color == color).length
            card_el.innerHTML = amount
        }
    }

    static render(data) {
        var player = data['players'][Game.getPlayerName()]
        this.renderChips(player.coins)
        this.renderCards(player.cards)
    }
}

class ScoreTable {

    static getTable() {
        return document.getElementById("score_table")
    }

    static getTBody() {
        return this.getTable().querySelector('tbody')
    }

    static initTable(players) {
        var table = this.getTBody()
        for (const [name, player] of Object.entries(players)) {
            let row = document.querySelector("#ScoreTableRowTemplate").content.cloneNode(true);
            row.firstElementChild.id = `sc_row_${name}`

            row.querySelector("#sc_name").innerHTML = name
            table.appendChild(row)
        }
    }

    static updateTable(players, active_player_name) {
        for (const [name, player] of Object.entries(players)) {
            let row = document.getElementById(`sc_row_${name}`)
            if (active_player_name == name) {
                row.classList.add("table-active")
            } else row.classList.remove("table-active")
            row.querySelector("#sc_score").innerHTML = player.getTotalScore()
            row.querySelector("#sc_black").innerHTML = `${player.getColorCardScore('black')} + ${player.coins["black"]}`
            row.querySelector("#sc_blue").innerHTML = `${player.getColorCardScore('blue')} + ${player.coins["blue"]}`
            row.querySelector("#sc_green").innerHTML = `${player.getColorCardScore('green')} + ${player.coins["green"]}`
            row.querySelector("#sc_red").innerHTML = `${player.getColorCardScore('red')} + ${player.coins["red"]}`
            row.querySelector("#sc_white").innerHTML = `${player.getColorCardScore('white')} + ${player.coins["white"]}`

        }
    }

    static render(data) {
        if (this.getTBody().children.length == 0) this.initTable(data.players)
        this.updateTable(data.players, data['current_player'])
    }
}

function render(data) {
    data = preprareData(data)
    Game.data = data
    console.log(data)
    Deck.render(data)
    MainPlayerDeck.render(data)
    ScoreTable.render(data)

}

function get_data() {
    RequestManager.getData(
        aUrl = `/api/player/${Game.getPlayerName()}/game`,
        aCallback = render,
        body = null,
    );
}

class Inter {
    static get_data_inter = null
    static get_data_time = 15000

    static get_data() {
        if (this.get_data_inter != null) clearInterval(this.get_data_inter)
        get_data()
        this.get_data_inter = setInterval(get_data, this.get_data_time)

    }

    static stop_get_data() {
        clearInterval(this.get_data_inter)
        this.get_data_inter = null
    }
}



function main() {
    Inter.get_data()
    // setInterval(get_data, 5000)
}
main();