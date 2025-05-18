document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form');
    const newPassword = document.getElementById('new-password');
    const confirmPassword = document.getElementById('confirm-password');
    const resetBtn = document.querySelector('.btnReset-popup');
  
    // Error container
    const errorContainer = document.createElement('div');
    errorContainer.className = 'error-container';
    form.insertBefore(errorContainer, form.querySelector('.navigation'));
  
    // Strength hint
    const hint = document.createElement('div');
    hint.className = 'password-hint';
    hint.innerHTML = `<p>Password must be at least <strong>8 characters</strong>.</p>`;
    form.insertBefore(hint, errorContainer);
  
    function showErrors(errors) {
      errorContainer.innerHTML = errors.map(msg => `
        <div class="error-message" style="color: #ff4444;">
          <i class="fas fa-exclamation-circle"></i> ${msg}
        </div>
      `).join('');
      setTimeout(() => {
        errorContainer.innerHTML = '';
      }, 6000);
    }
  
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const errors = [];
  
      const password = newPassword.value.trim();
      const confirm = confirmPassword.value.trim();
  
      // Validation
      if (!password) {
        errors.push("Password is required");
      } else if (password.length < 8) {
        errors.push("Password must be at least 8 characters");
      }
  
      if (!confirm) {
        errors.push("Confirm Password is required");
      } else if (password !== confirm) {
        errors.push("Passwords do not match");
      }
  
      if (errors.length > 0) {
        showErrors(errors);
        return;
      }
  
      // Simulate reset request
      try {
        resetBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Resetting...';
        resetBtn.disabled = true;
  
        const email = new URLSearchParams(window.location.search).get('email');
        const response = await fetch('https://your-backend-service.com/reset-password', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, newPassword: password })
        });
  
        if (!response.ok) throw new Error('Password reset failed');
  
        alert('Password reset successfully! Redirecting to login...');
        window.location.href = 'login.html';
  
      } catch (err) {
        showErrors([err.message]);
      } finally {
        resetBtn.innerHTML = 'Reset';
        resetBtn.disabled = false;
      }
    });
  });
  
  // Handle Log In button in header
  document.getElementById("loginBtn").addEventListener("click", () => {
    window.location.href = "login.html";
  });
  