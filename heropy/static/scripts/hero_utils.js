function Random(dice_number, base_value, id) {
    var rnd = 0;

    for (let i = 0; i < dice_number; i++) {
        rnd += Math.floor(Math.random() * 6) + 1;
    }

    document.getElementById(id).value = rnd + base_value;
}