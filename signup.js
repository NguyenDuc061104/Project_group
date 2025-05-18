document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("signup-form");
    const nameInput = document.getElementById("fullname");
    const emailInput = document.getElementById("email");
    const passwordInput = document.getElementById("password");
    const confirmInput = document.getElementById("confirm-password");
    const signupBtn = document.querySelector(".btnSignUp-popup");
    const errorContainer = form.querySelector(".error-container");
  
    // Toggle password visibility
    document.querySelectorAll(".toggle-password").forEach(button => {
      button.addEventListener("click", () => {
        const input = button.previousElementSibling;
        input.type = input.type === "password" ? "text" : "password";
        button.textContent = input.type === "password" ? "Show" : "Hide";
      });
    });
  
    function showErrors(errors) {
      errorContainer.innerHTML = errors.map(msg => `
        <div class="error-message">
          <i class="fas fa-exclamation-circle"></i> ${msg}
        </div>
      `).join("");
  
      setTimeout(() => {
        errorContainer.innerHTML = "";
      }, 6000);
    }
  
    async function checkEmailExists(email) {
      try {
        const response = await fetch(`/api/check-email?email=${encodeURIComponent(email)}`);
        const data = await response.json();
        return data.exists;
      } catch (err) {
        console.error("Email check error:", err);
        return false;
      }
    }
  
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const errors = [];
  
      const name = nameInput.value.trim();
      const email = emailInput.value.trim();
      const password = passwordInput.value;
      const confirmPassword = confirmInput.value;
  
      // Validation
      if (!name) {
        errors.push("Full name is required");
      } else if (/\d/.test(name)) {
        errors.push("Full name cannot contain numbers");
      }
  
      if (!email) {
        errors.push("Email is required");
      } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        errors.push("Invalid email address");
      }
  
      if (!password) {
        errors.push("Password is required");
      } else if (password.length < 8) {
        errors.push("Password must be at least 8 characters");
      }
  
      if (!confirmPassword) {
        errors.push("Confirm Password is required");
      } else if (password !== confirmPassword) {
        errors.push("Passwords do not match");
      }
  
      if (errors.length > 0) {
        showErrors(errors);
        return;
      }
  
      try {
        signupBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Checking...';
        const emailExists = await checkEmailExists(email);
        if (emailExists) {
          showErrors(["Email already registered"]);
          signupBtn.innerHTML = "Sign Up";
          return;
        }
  
        signupBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Registering...';
  
        const response = await fetch("/api/signup", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ name, email, password })
        });
  
        const data = await response.json();
  
        if (!response.ok) {
          showErrors([data.message || "Registration failed"]);
          signupBtn.innerHTML = "Sign Up";
          return;
        }
  
        localStorage.setItem("authToken", data.token);
        window.location.href = "/dashboard";
  
      } catch (error) {
        showErrors([error.message]);
      } finally {
        signupBtn.innerHTML = "Sign Up";
      }
    });
  
    // Password strength indicator
    passwordInput.addEventListener("input", () => {
      const strength = calculatePasswordStrength(passwordInput.value);
      const strengthBar = document.getElementById("strength-bar");
      const strengthText = document.getElementById("strength-text");
  
      if (!strengthBar || !strengthText) return;
  
      strengthBar.className = "password-strength";
      strengthText.textContent = "";
  
      if (strength === "weak") {
        strengthBar.classList.add("strength-weak");
        strengthText.textContent = "Weak password";
        strengthText.style.color = "#ff4d4d";
      } else if (strength === "medium") {
        strengthBar.classList.add("strength-medium");
        strengthText.textContent = "Moderate password";
        strengthText.style.color = "#ffa500";
      } else if (strength === "strong") {
        strengthBar.classList.add("strength-strong");
        strengthText.textContent = "Strong password";
        strengthText.style.color = "#4caf50";
      }
    });
  
    function calculatePasswordStrength(password) {
      if (password.length >= 12) return "strong";
      if (password.length >= 8) return "medium";
      return "weak";
    }
});
  
document.getElementById("loginBtn").addEventListener("click", () => {
    window.location.href = "login.html";
});