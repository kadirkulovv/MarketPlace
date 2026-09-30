/**
 * MARKETPLACE - CART JAVASCRIPT (AJAX INTERACTION)
 */

document.addEventListener('DOMContentLoaded', () => {
  const csrftoken = window.getCookie ? window.getCookie('csrftoken') : '';

  // 1. Quick Add To Cart from Product Cards / Detail Page
  document.querySelectorAll('.ajax-add-to-cart').forEach(button => {
    button.addEventListener('click', async (e) => {
      e.preventDefault();
      const productId = button.dataset.productId;
      const quantityInput = document.getElementById(`quantity-${productId}`);
      const quantity = quantityInput ? quantityInput.value : 1;

      const originalHtml = button.innerHTML;
      button.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
      button.disabled = true;

      try {
        const formData = new FormData();
        formData.append('quantity', quantity);
        formData.append('ajax', '1');

        const response = await fetch(`/cart/add/${productId}/`, {
          method: 'POST',
          headers: {
            'X-CSRFToken': csrftoken,
            'X-Requested-With': 'XMLHttpRequest'
          },
          body: formData
        });

        const data = await response.json();

        if (response.ok && data.status === 'success') {
          // Update navbar cart count
          const navBadges = document.querySelectorAll('.nav-cart-count');
          navBadges.forEach(badge => {
            badge.textContent = data.cart_count;
            badge.style.display = data.cart_count > 0 ? 'flex' : 'none';
          });

          if (window.showToast) {
            window.showToast(data.message, 'success');
          }
        } else {
          if (window.showToast) {
            window.showToast(data.message || 'Xatolik yuz berdi!', 'error');
          }
        }
      } catch (err) {
        console.error(err);
        if (window.showToast) {
          window.showToast('Server bilan bog\'lanishda xatolik!', 'error');
        }
      } finally {
        button.innerHTML = originalHtml;
        button.disabled = false;
      }
    });
  });

  // 2. Quantity Update (+ / -) in Cart Detail Page
  document.querySelectorAll('.btn-cart-qty').forEach(btn => {
    btn.addEventListener('click', async () => {
      const itemId = btn.dataset.itemId;
      const action = btn.dataset.action; // 'increase' or 'decrease'
      
      const formData = new FormData();
      formData.append('action', action);

      try {
        const response = await fetch(`/cart/update/${itemId}/`, {
          method: 'POST',
          headers: {
            'X-CSRFToken': csrftoken,
            'X-Requested-With': 'XMLHttpRequest'
          },
          body: formData
        });

        const data = await response.json();

        if (data.status === 'success' || data.status === 'warning') {
          // Update item quantity in DOM
          const qtyElement = document.getElementById(`item-qty-${itemId}`);
          if (qtyElement) qtyElement.textContent = data.item_quantity;

          // Update item subtotal
          const subtotalElement = document.getElementById(`item-total-${itemId}`);
          if (subtotalElement) subtotalElement.textContent = Number(data.item_total).toLocaleString('uz-UZ') + " so'm";

          // Update cart total
          updateCartTotals(data.cart_total, data.cart_count);

          if (data.status === 'warning' && window.showToast) {
            window.showToast(data.message, 'warning');
          }
        } else if (data.status === 'removed') {
          // Row was removed
          const row = document.getElementById(`cart-row-${itemId}`);
          if (row) row.remove();
          updateCartTotals(data.cart_total, data.cart_count);
          if (window.showToast) window.showToast(data.message, 'info');

          // Check if cart empty
          checkEmptyCart(data.cart_count);
        }
      } catch (err) {
        console.error(err);
      }
    });
  });

  // 3. Remove Item from Cart Button
  document.querySelectorAll('.btn-cart-remove').forEach(btn => {
    btn.addEventListener('click', async () => {
      const itemId = btn.dataset.itemId;
      if (!confirm('Ushbu mahsulotni savatdan o\'chirmoqchimisiz?')) return;

      try {
        const response = await fetch(`/cart/remove/${itemId}/`, {
          method: 'POST',
          headers: {
            'X-CSRFToken': csrftoken,
            'X-Requested-With': 'XMLHttpRequest'
          }
        });

        const data = await response.json();
        if (data.status === 'success') {
          const row = document.getElementById(`cart-row-${itemId}`);
          if (row) row.remove();

          updateCartTotals(data.cart_total, data.cart_count);
          if (window.showToast) window.showToast(data.message, 'info');
          checkEmptyCart(data.cart_count);
        }
      } catch (err) {
        console.error(err);
      }
    });
  });

  function updateCartTotals(totalPrice, totalCount) {
    const totalEls = document.querySelectorAll('.cart-total-price');
    totalEls.forEach(el => {
      el.textContent = Number(totalPrice).toLocaleString('uz-UZ') + " so'm";
    });

    const navBadges = document.querySelectorAll('.nav-cart-count');
    navBadges.forEach(badge => {
      badge.textContent = totalCount;
      badge.style.display = totalCount > 0 ? 'flex' : 'none';
    });
  }

  function checkEmptyCart(count) {
    if (count <= 0) {
      const cartTableWrap = document.getElementById('cart-content-wrapper');
      const emptyWrap = document.getElementById('cart-empty-wrapper');
      if (cartTableWrap) cartTableWrap.style.display = 'none';
      if (emptyWrap) emptyWrap.style.display = 'block';
    }
  }
});
