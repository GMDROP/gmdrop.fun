
if (!localStorage.getItem('balanse')) {
    localStorage.setItem('balanse', 0)   
}

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
