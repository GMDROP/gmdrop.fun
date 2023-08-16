$('.modal').click(() => {
    $('.modal').css('display', 'none')
})

$('#pop_').click(() => {
    $('#modal_one').css('display', 'block')
})
$('#viv_').click(() => {
    $('#modal_two').css('display', 'block')
})

setInterval(() => {
    $('.balance_id').text(localStorage.getItem('balanse'))
}, 1000)
$('#price').click(() => {
    let num = Number(localStorage.getItem('balanse'))
    localStorage.setItem('balanse', num + 10)
})

let text = localStorage.getItem("weapons");
let obj = JSON.parse(text);

$.map(obj, function (elementOrValue, indexOrKey) {
    $('#weapons_id').append(`
    <div class="item">
            <img src="${elementOrValue.img}" alt="" />
            <p>${elementOrValue.name}</p>
          </div>
    `);
});