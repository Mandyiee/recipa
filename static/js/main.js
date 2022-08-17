const first = document.getElementById('first')
const second = document.getElementById('second')
const third = document.getElementById('third')
const fourth = document.getElementById('fourth')
const fifth = document.getElementById('fifth')

const arr = [first, second, third, fourth, fifth]

const input = document.querySelector('.button-star-rating')

const stars = document.querySelectorAll('.button-star')

function starSelect(id) {
    stars.forEach(item => {
        if (item.getAttribute('data-star-id') <= id) {
            item.classList.add('checked')

        } else {
            item.classList.remove('checked')
        }
        input.value = Number(id)

    })
}

arr.forEach(item => {
    item.addEventListener('mouseover', (event) => {
        starSelect(item.getAttribute('data-star-id'))
    })
})