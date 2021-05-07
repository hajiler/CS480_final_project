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

function showSlots() {
    $('#info_area').empty();
    const query = '/schedule?type=nurse';
    $('#form_time_Register').empty();
    fetch(query)
        .then(response => response.json())
        .then(json => {
            for (let id in json.times) {
                const slot = json.times[parseInt(id)];
                let card = $('<div>', {class: 'card'});
                let cardBody = $('<div>', {class: 'card-body'});
                cardBody.text(slot);

                card.append(cardBody);
                $('#form_time_Register').append(card);
                const postQuery = '/schedule?type=nurse&inputSlot=' + slot;
                card.click(function () {

                    $.post(postQuery);
                });
            }
            $('div.card').mouseenter( function () {
                $(this).addClass("card bg-dark text-white");
            }).mouseleave( function () {
                $(this).removeClass("card bg-dark text-white");
                $(this).addClass("card");
            })
            getForm('time','Register');
        });

}

function showMySlots() {
    $('#info_area').empty();
    const query = '/schedule?type=nurse&Personal=true';
    $('#form_time_Update').empty();
    fetch(query)
        .then(response => response.json())
        .then(json => {
            for (let id in json.times) {
                console.log(json.times)
                const slot = json.times[parseInt(id)];
                let card = $('<div>', {class: 'card'});
                let cardBody = $('<div>', {class: 'card-body'});
                cardBody.text(slot);

                card.append(cardBody);
                $('#form_time_Update').append(card);
                const postQuery = '/schedule?action=Remove&type=nurse&inputSlot=' + slot;
                card.click(function () {
                    $.post(postQuery);
                });
            }
            $('div.card').mouseenter( function () {
                $(this).addClass("card bg-dark text-white");
            }).mouseleave( function () {
                $(this).removeClass("card bg-dark text-white");
                $(this).addClass("card");
            })
            getForm('time','Update');
        });
}

function getSelf() {
    const id = $('#inputID_fetch').val();
    console.log(id);
    $('#info_area').empty();
    const query = '/view?type=Nurse'
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