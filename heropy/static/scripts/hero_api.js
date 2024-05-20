DEFAULT_FETCH_HEADER =  {
    'Accept': 'application/json',
    'X-Requested-With': 'XMLHttpRequest',
}

function callApi(fetchUrl, fetchHeaders, updateCallback) {
    fetch(
        fetchUrl, fetchHeaders
    ).then(response => {
        return response.json()
    }).then(responseData => {
        updateCallback(responseData)
    })
}

function updateStat(stat, value) {
    callApi(`/heropy/stat/${stat}/${value}`, DEFAULT_FETCH_HEADER, (responseData) => {
        document.getElementById(`${stat}Field`).textContent = (stat == "gold" ? responseData[stat] : responseData['stats'][stat]);
    })
}

function updateInventory() {
    callApi(``, DEFAULT_FETCH_HEADER, (responseData) => {
        var container = document.getElementById(`inventoryDiv`);

        container.innerHTML = "";

        var className = ""

        // TODO
    })
}

function updateSpell() {
    callApi(``, DEFAULT_FETCH_HEADER, (responseData) => {
        var container = document.getElementById(`spellDiv`);

        container.innerHTML = "";

        var className = ""

        // TODO
    })
}