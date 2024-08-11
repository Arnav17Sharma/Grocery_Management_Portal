let delButtons = document.getElementsByClassName('del-btn');
let conButtons = document.getElementsByClassName('con-btn');
let data = document.getElementById('data')

// console.log(delButtons)


for (let button of delButtons) {
    button.addEventListener('click', () => {
        var clickedElement = event.target
        var clickedRow = clickedElement.parentNode.parentNode.id;
        var rowData = document.getElementById(clickedRow).querySelectorAll('.column-data');
        let prodID = rowData[0].innerHTML
        console.log(prodID)
        data.value = parseInt(prodID)
    });
}