let allButtons = document.getElementsByClassName('add-inp');
let removeAllButtons = document.getElementsByClassName('remove-inp');
let rows = document.querySelectorAll('.total')
let rowList = document.querySelectorAll('.rows')
let total = document.getElementById('total')
let data = document.getElementById('data')


for (let button of allButtons) {
    button.addEventListener('click', () => {
        let sum = 0
        var clickedElement = event.target
        var clickedRow = clickedElement.parentNode.parentNode.id;
        var rowData = document.getElementById(clickedRow).querySelectorAll('.column-data');
        // console.log(rowData)
        let prodID = rowData[0].innerHTML
        let prodName = rowData[1].innerHTML
        let priceUnit = rowData[3].innerHTML
        rowData[6].innerHTML = parseInt(rowData[6].innerHTML)+1
        rowData[7].innerHTML = parseInt(rowData[6].innerHTML) * priceUnit
        for(let i of rows){
            sum += parseInt(i.innerHTML)
        }
        total.value = sum
        console.log(prodID)
        console.log(prodName)
        console.log(priceUnit)
        console.log(rowData[6].innerHTML)
        console.log(rowData[7].innerHTML)
    });
}

for (let button of removeAllButtons) {
    button.addEventListener('click', () => {
        let sum = 0
        var clickedElement = event.target
        var clickedRow = clickedElement.parentNode.parentNode.id;
        var rowData = document.getElementById(clickedRow).querySelectorAll('.column-data')
        // console.log(rowData)
        let prodID = rowData[0].innerHTML
        let prodName = rowData[1].innerHTML
        let priceUnit = parseFloat(rowData[3].innerHTML)
        rowData[6].innerHTML = Math.max(0, parseInt(rowData[6].innerHTML)-1)
        rowData[7].innerHTML = parseInt(rowData[6].innerHTML) * priceUnit
        for(let i of rows){
            sum += parseInt(i.innerHTML)
        }
        total.value = sum
        console.log(prodID)
        console.log(prodName)
        console.log(priceUnit)
        console.log(rowData[6].innerHTML)
        console.log(rowData[7].innerHTML)
    });
}

let submitBtn = document.getElementById('submitBtn')

function helper() {
    let orderDetails = []
    // console.log(rowList)
    for(let row in rowList) {
        if (!rowList.hasOwnProperty(row)) continue;
        // console.log(typeof row)
        // console.log(row)
        productDetails = {}
        // let rowID = parseInt(row)+1
        // console.log(rowID)
        // let rowData = document.getElementById('prodRow' + rowID)
        let rowData = rowList[row].querySelectorAll('.column-data')
        // console.log(parseInt(rowData[0].innerHTML))
        let product_id = parseInt(rowData[0].innerHTML)
        let quantity = parseInt(rowData[6].innerHTML)
        let total_price = parseFloat(rowData[7].innerHTML)
        // console.log(rowData)
        productDetails.product_id = product_id
        productDetails.quantity = quantity
        productDetails.total_price = total_price
        if(quantity != 0){orderDetails.push(productDetails)}
        // console.log(productDetails)
    }
    console.log(orderDetails)
    data.value = JSON.stringify(orderDetails)
    // return orderDetails
    // $.ajax({
    //     url: "/insertOrder",
    //     type: "POST",
    //     data: JSON.stringify({1:orderDetails})
    // });
}
