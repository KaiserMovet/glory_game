
function getPlayerName() {
    let player_name = window.location.pathname.split('/')[2];
    return player_name
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
    return data

}

function renderDeck(data) {
    for (let level of ['1', '2', '3']) {
        let cards = data['deck'][level]
        console.log(level)
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
            if (current_id_list.includes(card.obj_id)) {
                continue
            }
            deck_div.append(card.getHTML())
        }
    }
}
function render(data) {
    data = preprareData(data)
    console.log(data)
    renderDeck(data)
}

function get_data() {
    RequestManager.getData(
        aUrl = `/api/player/${getPlayerName()}/game`,
        aCallback = render,
        body = null,
    );
}

function main() {
    get_data()
    // setInterval(get_data, 5000)
}
main();