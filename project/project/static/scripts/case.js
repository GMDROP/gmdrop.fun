const cells = 31

// From 0.001 to 100
const items = [
  { name: 'M 60', img: 'https://ggstandoff.app/public/storage/items/1688133750cde0a62e5151a5ad293c8c4731597eeb.png', chance: 10 },
  { name: 'Glock', img: 'https://ggstandoff.app/public/storage/items/16507405721e1ee2abcb5d925d38e1335ee7991ab4.png', chance: 25 },
  { name: 'FFFF', img: 'https://ggstandoff.app/public/storage/items/16880814769284e51f2117dac4649bdccbd673becc.png', chance: 40 }
]

function getItem() {
  let item;

  while (!item) {
    const chance = Math.floor(Math.random() * 100)

    items.forEach(elm => {
      if (chance < elm.chance && !item) item = elm
    })
  }

  return item
}

function generateItems() {
  document.querySelector('.list').remove()
  document.querySelector('.scope').innerHTML = `
    <ul class="list"></ul>
  `

  const list = document.querySelector('.list')

  for (let i = 0; i < cells; i++) {
    const item = getItem()

    const li = document.createElement('li')
    li.setAttribute('data-item', JSON.stringify(item))
    li.classList.add('list__item')
    li.innerHTML = `
      <img src="${item.img}" alt="" />
    `

    list.append(li)
  }
}

generateItems()

let isStarted = false
let isFirstStart = true

function start(i) {
  if (Number(i) <= Number(localStorage.getItem('balanse'))) {
    let num = Number(localStorage.getItem('balanse'))
    localStorage.setItem('balanse', num - i)

    if (isStarted) return
    else isStarted = true

    if (!isFirstStart) generateItems()
    else isFirstStart = false
    const list = document.querySelector('.list')

    setTimeout(() => {
      list.style.left = '50%'
      list.style.transform = 'translate3d(-50%, 0, 0)'
    }, 0)

    const item = list.querySelectorAll('li')[15]

    list.addEventListener('transitionend', () => {
      isStarted = false
      item.classList.add('active')
      const data = JSON.parse(item.getAttribute('data-item'))
      if (!localStorage.getItem('weapons')) {
        localStorage.setItem('weapons', JSON.stringify([]))
      }

      let weapons = []

      let text = localStorage.getItem("weapons");
      let obj = JSON.parse(text);

      $.map(obj, function (elementOrValue, indexOrKey) {
        weapons.push(elementOrValue)
      });

      weapons.push(data)

      localStorage.setItem('weapons', JSON.stringify(weapons))

      console.log(data);
    }, { once: true })
  }
}