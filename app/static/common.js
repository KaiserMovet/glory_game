var RequestManager = {

    HttpClient: function () {
        this.get = function (method, aUrl, aCallback, body, ...args) {
            var anHttpRequest = new XMLHttpRequest();
            anHttpRequest.onreadystatechange = function () {
                if (anHttpRequest.readyState == 4 && 200 <= anHttpRequest.status < 300)
                    aCallback(JSON.parse(anHttpRequest.responseText), ...args);
            }

            anHttpRequest.open(method, aUrl, true);
            anHttpRequest.setRequestHeader("Content-Type", "application/json")
            anHttpRequest.send(JSON.stringify(body));
        }
    },

    getData: function (aUrl, aCallback, body, ...args) {
        local = window.location.origin;
        var client = new this.HttpClient();
        client.get(method = "GET", local + aUrl, aCallback, body, ...args);

    },

    postData: function (aUrl, aCallback, body, ...args) {
        local = window.location.origin;
        var client = new this.HttpClient();
        client.get(method = "POST", local + aUrl, aCallback, body, ...args);

    },
}