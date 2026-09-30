/**
 * MARKETPLACE - DASHBOARD JAVASCRIPT (SELLER CONTROLS)
 */

document.addEventListener('DOMContentLoaded', () => {
  const csrftoken = window.getCookie ? window.getCookie('csrftoken') : '';

  // 1. Inline Quick Stock Update Form
  document.querySelectorAll('.stock-quick-form').forEach(form => {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const productId = form.dataset.productId;
      const input = form.querySelector('.stock-input');
      const submitBtn = form.querySelector('.stock-save-btn');
      const newStock = input.value;

      const originalHtml = submitBtn.innerHTML;
      submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
      submitBtn.disabled = true;

      try {
        const formData = new FormData();
        formData.append('stock', newStock);

        const response = await fetch(`/dashboard/products/${productId}/stock/`, {
          method: 'POST',
          headers: {
            'X-CSRFToken': csrftoken,
            'X-Requested-With': 'XMLHttpRequest'
          },
          body: formData
        });

        const data = await response.json();
        if (response.ok && data.status === 'success') {
          input.value = data.stock;
          submitBtn.style.background = 'var(--success)';
          submitBtn.innerHTML = '<i class="fas fa-check"></i>';
          setTimeout(() => {
            submitBtn.style.background = '';
            submitBtn.innerHTML = originalHtml;
            submitBtn.disabled = false;
          }, 1500);

          if (window.showToast) {
            window.showToast(`Ombor qoldig'i ${data.stock} donaga yangilandi!`, 'success');
          }
        } else {
          submitBtn.innerHTML = originalHtml;
          submitBtn.disabled = false;
          if (window.showToast) {
            window.showToast('Qoldiqni yangilashda xatolik yuz berdi!', 'error');
          }
        }
      } catch (err) {
        console.error(err);
        submitBtn.innerHTML = originalHtml;
        submitBtn.disabled = false;
        if (window.showToast) {
          window.showToast('Tarmoqda xatolik yuz berdi!', 'error');
        }
      }
    });
  });

  // 2. Image preview on file input change
  const imageInput = document.querySelector('input[type="file"][name="main_image"]');
  if (imageInput) {
    imageInput.addEventListener('change', function() {
      if (this.files && this.files[0]) {
        const reader = new FileReader();
        reader.onload = function(e) {
          let preview = document.getElementById('image-preview');
          if (!preview) {
            preview = document.createElement('img');
            preview.id = 'image-preview';
            preview.style.maxHeight = '180px';
            preview.style.borderRadius = '12px';
            preview.style.marginTop = '12px';
            imageInput.parentNode.appendChild(preview);
          }
          preview.src = e.target.result;
        };
        reader.readAsDataURL(this.files[0]);
      }
    });
  }
});
