document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector(".login form");
    const emailInput = form.querySelector("input[type='email']");
    const passwordInput = form.querySelector("input[type='password']");
    const loginBtn = document.querySelector(".btnLogin-popup");
    const errorContainer = document.createElement("div");
    errorContainer.className = "error-container";
    form.prepend(errorContainer);

    // Real-time validation
    emailInput.addEventListener("input", validateForm);
    passwordInput.addEventListener("input", validateForm);

    function showError(message) {
        errorContainer.innerHTML = `
            <div class="error-message">
                <i class="fas fa-exclamation-circle"></i>
                ${message}
            </div>
        `;
        setTimeout(() => errorContainer.innerHTML = "", 5000);
    }

    function validateForm() {
        const emailValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(emailInput.value);
        const passwordValid = passwordInput.value.length >= 8;
        
        loginBtn.disabled = !(emailValid && passwordValid);
        return emailValid && passwordValid;
    }

    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        
        if (!validateForm()) {
            showError("Please fix the form errors before submitting");
            return;
        }

        try {
            loginBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Logging in...';
            const response = await fetch("/api/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    email: emailInput.value,
                    password: passwordInput.value
                })
            });

            const data = await response.json();
            
            if (!response.ok) throw new Error(data.message || "Login failed");
            
            // Store JWT and redirect
            localStorage.setItem("authToken", data.token);
            window.location.href = "/dashboard";
        } catch (error) {
            showError(error.message);
        } finally {
            loginBtn.innerHTML = "Log In";
        }
    });

    // Google OAuth handler
    document.querySelector(".google-login").addEventListener("click", (e) => {
        e.preventDefault();
        window.location.href = "/auth/google";
    });
      
});

document.getElementById("signupBtn").addEventListener("click", () => {
    window.location.href = "signup.html";
});
