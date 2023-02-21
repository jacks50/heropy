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
        var container = document.getElementById(`${stat}Div`);

        container.innerHTML = "";

        var className = ""

        switch(stat) {
            case 'endurance':
                className = "nes-icon is-small heart";
                break;
            case 'dexterity':
                className = "nes-icon is-small trophy";
                break;
            case 'luck':
                className = "nes-icon is-small star";
                break;
        }

        statValue = responseData[stat]

        if (statValue > 20) {
            var elem = document.createElement("i");
            elem.className = className;
            elem.innerText = "x" + statValue;
            container.appendChild(elem);
        } else {
            for (let i = 0; i < statValue; i++) {
                var elem = document.createElement("i");
                elem.className = className;
                container.appendChild(elem);
            }
        }
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