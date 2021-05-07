function setup() {
    $(document).ready(function () {
        $('a.nav-item').click(function () {
            $(this).siblings().fadeToggle();
        });
    });
}

function getForm(type, kind) {
    $('#info_area').empty();
    $('form').slideUp();
    const query = `#form_${type}_${kind}`;
    console.log(query);
    $(query).slideToggle();
}

function getNurse() {
    const id = $('#inputID_fetch').val();
    console.log(id);
    $('#info_area').empty();
    const query = '/view?type=Nurse&inputID=' + id;
    fetch(query)
        .then(response => response.json())
        .then(json => {
            console.log(json);
            for (let key in json) {
                console.log(key);
                const value = json[key];
                const node = $('<p>');
                node.text(value);
                $('#info_area').append(node);
            }
        });
}

function getPatient() {
    const id = $('#inputSSN_fetch').val();
    console.log(id);
    $('#info_area').empty();
    const query = '/view?type=patient&inputSSN=' + id;
    fetch(query)
        .then(response => response.json())
        .then(json => {
            console.log(json);
            for (let key in json) {
                console.log(key);
                const value = json[key];
                const node = $('<p>');
                node.text(value);
                $('#info_area').append(node);
            }
        });
}

function getVaccine() {
    const id = $('#inputName_fetch').val();
    console.log(id);
    $('#info_area').empty();
    const query = '/view?type=vaccine&inputName=' + id;
    fetch(query)
        .then(response => response.json())
        .then(json => {
            console.log(json);
            for (let key in json) {
                console.log(key);
                const value = json[key];
                const node = $('<p>');
                node.text(value);
                $('#info_area').append(node);
            }
        });
}
