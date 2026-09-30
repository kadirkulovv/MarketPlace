/**
 * MARKETPLACE - AUTHENTICATION INTERACTION (ROLE SWITCHER)
 */

document.addEventListener('DOMContentLoaded', () => {
  const roleSelect = document.querySelector('select[name="role"]');
  const shopNameGroup = document.getElementById('div_id_shop_name') || document.querySelector('.shop-name-group');

  function toggleShopName() {
    if (!roleSelect || !shopNameGroup) return;
    if (roleSelect.value === 'seller') {
      shopNameGroup.style.display = 'block';
      const input = shopNameGroup.querySelector('input');
      if (input) input.required = true;
    } else {
      shopNameGroup.style.display = 'none';
      const input = shopNameGroup.querySelector('input');
      if (input) input.required = false;
    }
  }

  if (roleSelect) {
    roleSelect.addEventListener('change', toggleShopName);
    toggleShopName(); // initial check
  }

  // Password toggle visibility
  document.querySelectorAll('.password-toggle').forEach(btn => {
    btn.addEventListener('click', () => {
      const input = btn.previousElementSibling;
      if (input && input.type === 'password') {
        input.type = 'text';
        btn.innerHTML = '<i class="fas fa-eye-slash"></i>';
      } else if (input) {
        input.type = 'password';
        btn.innerHTML = '<i class="fas fa-eye"></i>';
      }
    });
  });
});
