


function addPlayer() {
    let player_name = document.getElementById("player_name").value;
    PLAYER = player_name
    RequestManager.postData("/api/new", console.log, { "name": player_name })
    document.getElementById('ready_button').disabled = true;
    setInterval(openGameIfReady, 1000, player_name);

}

function showPlayers() {

    function printPlayers(data) {
        let span = document.getElementById("players");
        span.innerHTML = data['response']['players'];
    }
    RequestManager.getData(
        aUrl = "/api/new_players",
        aCallback = printPlayers,
        body = null);

}

function openGameIfReady(player_name) {


    function redirectToGame(body, player_name) {
        local = window.location.origin;
        window.location.href = `${local}/player/${player_name}/game`;
    }
    RequestManager.getData(
        aUrl = `/api/player/${player_name}/game`,
        aCallback = redirectToGame,
        body = null,
        player_name = player_name);
}

function createGame() {
    document.getElementById('start_button').disabled = true;
    RequestManager.getData(
        aUrl = `/api/new_game`,
        aCallback = null,
        body = null);
}

function main() {

    setInterval(showPlayers, 1000);
}

main()