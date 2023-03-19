function RollDice(dice_number) {
    var rnd = 0;

    for (let i = 0; i < dice_number; i++) {
        rnd += Math.floor(Math.random() * 6) + 1;
    }

    return rnd;
}

function Random(dice_number, base_id, target_id) {
    var base_value = 0;

    if (document.getElementById(base_id).hasAttribute('value')) {
        base_value = parseInt(document.getElementById(base_id).value);
        var rnd = RollDice(dice_number);
        document.getElementById(target_id).value = rnd + base_value;
    } else {
        base_value = parseInt(document.getElementById(base_id).textContent);
        var rnd = RollDice(dice_number);
        document.getElementById(target_id).innerHTML = rnd + base_value;
    }
}