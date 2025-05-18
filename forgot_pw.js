document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('.signup form');
    const emailInput = document.querySelector('input[type="email"]');
    const submitBtn = document.querySelector('.btnSignUp-popup');
    const errorContainer = document.createElement('div');
    errorContainer.className = 'error-container';
    form.insertBefore(errorContainer, form.querySelector('.navigation'));
  
    const showError = (message) => {
      errorContainer.innerHTML = `
        <div class="error-message" style="color: #ff4444;">
          <i class="fas fa-exclamation-circle"></i> ${message}
        </div>
      `;
      setTimeout(() => errorContainer.innerHTML = "", 5000);
    };
  
    const allowedDomains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com"];
  
    function validateEmail(email) {
      const basicFormat = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!email) return "Email cannot be empty";
      if (!basicFormat.test(email)) return "Please enter a valid email format";
  
      return null; // valid
    }
  
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      errorContainer.innerHTML = "";
  
      const email = emailInput.value.trim();
      const validationMessage = validateEmail(email);
      if (validationMessage) {
        showError(validationMessage);
        return;
      }
  
      try {
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';
        submitBtn.disabled = true;
  
        const response = await fetch('https://your-backend-service.com/send-reset-email', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email }),
        });
  
        if (!response.ok) throw new Error('Failed to send reset email');
  
        window.location.href = 'reset_password.html?email=' + encodeURIComponent(email);
      } catch (error) {
        showError(error.message);
      } finally {
        submitBtn.innerHTML = "Get Link!";
        submitBtn.disabled = false;
      }
    });
  
    // ---------- Utility functions ----------
    function levenshteinDistance(a, b) {
      const dp = Array.from({ length: a.length + 1 }, () => Array(b.length + 1).fill(0));
      for (let i = 0; i <= a.length; i++) dp[i][0] = i;
      for (let j = 0; j <= b.length; j++) dp[0][j] = j;
  
      for (let i = 1; i <= a.length; i++) {
        for (let j = 1; j <= b.length; j++) {
          if (a[i - 1] === b[j - 1]) {
            dp[i][j] = dp[i - 1][j - 1];
          } else {
            dp[i][j] = 1 + Math.min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]);
          }
        }
      }
  
      return dp[a.length][b.length];
    }
  
    function closestDomain(domain) {
      let minDist = Infinity;
      let closest = "";
      allowedDomains.forEach(d => {
        const dist = levenshteinDistance(domain, d);
        if (dist < minDist) {
          minDist = dist;
          closest = d;
        }
      });
      return closest;
    }
});

document.getElementById("loginBtn").addEventListener("click", () => {
    window.location.href = "login.html";
});  