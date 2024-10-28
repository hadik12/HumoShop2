document.addEventListener('DOMContentLoaded', function() {
    // Обработка изменения количества
    document.querySelectorAll('.quantity-controls').forEach(control => {
        const input = control.querySelector('.quantity-input');
        const decrease = control.querySelector('.decrease');
        const increase = control.querySelector('.increase');

        decrease.addEventListener('click', () => {
            if (input.value > 1) {
                input.value = parseInt(input.value) - 1;
                updateCartItem(control.closest('.cart-item'));
            }
        });

        increase.addEventListener('click', () => {
            input.value = parseInt(input.value) + 1;
            updateCartItem(control.closest('.cart-item'));
        });

        input.addEventListener('change', () => {
            if (input.value < 1) input.value = 1;
            updateCartItem(control.closest('.cart-item'));
        });
    });
});

function updateCartItem(cartItem) {
    const itemId = cartItem.dataset.itemId;
    const quantity = cartItem.querySelector('.quantity-input').value;

    fetch('/cart/update/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: `item_id=${itemId}&quantity=${quantity}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            cartItem.querySelector('.price').textContent = data.total + ' ₽';
            updateCartTotal();
        }
    });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i  < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function updateCartTotal() {
    const cartItems = document.querySelectorAll('.cart-item');
    let total = 0;
    cartItems.forEach(item => {
        total += parseInt(item.querySelector('.price').textContent.replace(' ₽', ''));
    });
    document.querySelector('.cart-total h2').textContent = `Итого: ${total} ₽`;
}