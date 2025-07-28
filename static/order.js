document.addEventListener('DOMContentLoaded', function () {
    // This object will hold the current state of our order
    const orderState = [];

    // 1. INITIALIZE STATE from the HTML table
    function initializeState() {
        document.querySelectorAll('#order-table-body tr').forEach(row => {
            const productId = parseInt(row.dataset.productId, 10);
            const price = parseFloat(row.querySelector('.price-per-unit').innerText);
            
            if (!isNaN(productId)) {
                orderState.push({
                    id: productId,
                    price: price,
                    quantity: 0
                });
            }
        });
    }

    // 2. RENDER FUNCTION: Updates the UI based on the current state
    function render() {
        let grandTotal = 0;

        orderState.forEach(item => {
            const row = document.querySelector(`tr[data-product-id='${item.id}']`);
            if (row) {
                const itemTotal = item.quantity * item.price;
                grandTotal += itemTotal;

                row.querySelector('.quantity').innerText = item.quantity;
                row.querySelector('.item-total').innerText = itemTotal.toFixed(2);
            }
        });

        // Update Grand Total in the UI
        document.getElementById('grand-total').innerText = grandTotal.toFixed(2);

        // Prepare data for form submission
        const orderDetailsForSubmission = orderState
            .filter(item => item.quantity > 0)
            .map(item => ({
                product_id: item.id,
                quantity: item.quantity,
                total_price: item.quantity * item.price
            }));

        // Update the hidden form inputs
        document.getElementById('data').value = JSON.stringify(orderDetailsForSubmission);
        document.getElementById('total').value = grandTotal;
    }

    // 3. EVENT LISTENER using Event Delegation
    document.getElementById('order-table-body').addEventListener('click', function (event) {
        // Check if a quantity button was clicked
        const button = event.target.closest('.btn-quantity');
        if (!button) return;

        const row = event.target.closest('tr');
        const productId = parseInt(row.dataset.productId, 10);
        const change = parseInt(button.dataset.change, 10);

        // Find the item in our state
        const itemInState = orderState.find(item => item.id === productId);

        if (itemInState) {
            // Update the quantity in the state (ensuring it doesn't go below 0)
            itemInState.quantity = Math.max(0, itemInState.quantity + change);
            
            // Re-render the UI
            render();
        }
    });

    // Run the initialization
    initializeState();
});