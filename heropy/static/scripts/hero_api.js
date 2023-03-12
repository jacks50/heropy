DEFAULT_FETCH_HEADER =  {
    'Accept': 'application/json',
    'X-Requested-With': 'XMLHttpRequest',
}

function CallApi(fetchUrl, fetchHeaders, updateCallback) {
    fetch(
        fetchUrl, fetchHeaders
    ).then(response => {
        return response.json()
    }).then(responseData => {
        updateCallback(responseData)
    })
}

function UpdateStats(stat, value) {
    CallApi(`/heropy/stat/${stat}/${value}`, DEFAULT_FETCH_HEADER, (responseData) => {
        var i = document.getElementById(`${stat}Field`);
        i.textContent = "x " + responseData[stat];
    })
}

function UpdateInventory() {
    CallApi(``, DEFAULT_FETCH_HEADER, (responseData) => {
        var container = document.getElementById(`inventoryDiv`);

        container.innerHTML = "";

        var className = ""

        // TODO
    })
}