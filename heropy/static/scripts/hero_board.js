/* ---------- GOLD DIALOG ----------- */
function showGoldDialog() {
    document.getElementById("goldInput").value = "0";
    document.getElementById("goldDialog").showModal();
}

function confirmGold() {
    const goldInput = document.getElementById("goldInput");
    updateStat('gold', goldInput.value);
    goldDialog.close();
}

function closeGoldDialog() {
    goldDialog.close();
}

/* ---------- ITEM DIALOG ----------- */
function showInventoryDialog() {
    document.getElementById("inventoryDialog").showModal();
}

function openTab(event, tabName) {
    var i, tabcontent, tablinks;

    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    document.getElementById(tabName).style.display = "block";
    event.currentTarget.className += "active";
}

function showItemDialog() {
    document.getElementById("itemDialog").showModal();
}

function confirmItemDialog() {
    document.getElementById("itemDialog").close();
}

function closeItemDialog() {
    document.getElementById("itemDialog").close();
}

/* ---------- SPELL DIALOG ----------- */
function showSpellDialog() {
    document.getElementById("spellDialog").showModal();
}

function confirmSpellDialog() {
    document.getElementById("spellDialog").close();
}

function closeSpellDialog() {
    document.getElementById("spellDialog").close();
}