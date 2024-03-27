document.addEventListener('DOMContentLoaded', function() {
    const quantityInputs = document.querySelectorAll('.item-quantity');
    quantityInputs.forEach(input => {
        input.addEventListener('change', function() {
            const cartItemId = this.dataset.cartitemId;
            const newQuantity = this.value;
            updateCartItem(cartItemId, newQuantity);
        });
    });

    const deleteButtons = document.querySelectorAll('.delete-item-btn');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function() {
            const cartItemId = this.dataset.cartitemId;
            deleteCartItem(cartItemId);
        });
    });

    // Функция для обновления количества товара в корзине
    function updateCartItem(cartItemId, quantity) {
        fetch('/cart/update_cart_item/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({
                'cart_item_id': cartItemId,
                'quantity': quantity
            }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Обновляем информацию на странице или выполняем другие действия
                console.log('Количество товара обновлено успешно');
            }
        })
        .catch(error => console.error('Ошибка:', error));
    }

    // Функция для удаления товара из корзины
    function deleteCartItem(cartItemId) {
        fetch('/cart/delete_cart_item/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({
                'cart_item_id': cartItemId
            }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log('Товар удален из корзины успешно');
                location.reload(); // Обновляем страницу
            }
        })
        .catch(error => console.error('Ошибка:', error));
    }

    // Функция для получения CSRF-токена из куки
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
    }
});

    function getCSRFToken() {
    const cookieValue = document.cookie.match('(^|;)\\s*' + 'csrftoken' + '\\s*=\\s*([^;]+)');
    return cookieValue ? cookieValue.pop() : '';
}