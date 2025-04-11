  // 👉 1. Tính tổng tiền theo số lượng sản phẩm
  const quantityInputs = document.querySelectorAll('.quantity-input');
  const subtotalSpan = document.querySelector('.summary p span');
  const totalSpan = document.querySelector('.summary p:last-child span');
  const prices = [125900, 48000]; // Giá sản phẩm dạng số (tương ứng với vị trí)

  function updateTotal() {
    let subtotal = 0;
    quantityInputs.forEach((input, index) => {
      const quantity = parseInt(input.value);
      subtotal += prices[index] * quantity;
    });

    const formatted = subtotal.toLocaleString('vi-VN') + 'đ';
    subtotalSpan.textContent = formatted;
    totalSpan.textContent = formatted;
  }

  // Khi người dùng thay đổi số lượng
  quantityInputs.forEach(input => {
    input.addEventListener('input', updateTotal);
  });

  // 👉 2. Kiểm tra hợp lệ form
  function validateForm() {
    const requiredFields = [
      { id: 'first-name', name: 'First Name' },
      { id: 'last-name', name: 'Last Name' },
      { id: 'state', name: 'State/Province' },
      { id: 'city', name: 'City' },
      { id: 'address', name: 'Address' },
      { id: 'phone', name: 'Phone' },
      { id: 'email', name: 'Email' }
    ];

    for (let field of requiredFields) {
      const input = document.getElementById(field.id);
      if (!input.value.trim()) {
        alert(`Please enter your ${field.name}.`);
        input.focus();
        return false;
      }
    }

    // Kiểm tra định dạng email đơn giản
    const emailInput = document.getElementById('email');
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(emailInput.value)) {
      alert("Please enter a valid email address.");
      emailInput.focus();
      return false;
    }

    return true;
  }

  // 👉 3. Xử lý khi đặt hàng
  function handleOrder() {
    if (!validateForm()) return;

    // Lấy thông tin người dùng
    const userInfo = {
      firstName: document.getElementById('first-name').value,
      lastName: document.getElementById('last-name').value,
      state: document.getElementById('state').value,
      city: document.getElementById('city').value,
      address: document.getElementById('address').value,
      phone: document.getElementById('phone').value,
      email: document.getElementById('email').value
    };

    // Lấy sản phẩm và số lượng
    const productList = [
      {
        name: "Super soft Capybara plush",
        price: prices[0],
        quantity: parseInt(quantityInputs[0].value)
      },
      {
        name: "Jellycat Bunny Rabbit",
        price: prices[1],
        quantity: parseInt(quantityInputs[1].value)
      }
    ];

    const total = productList.reduce((acc, item) => acc + item.price * item.quantity, 0);

    // 👉 4. Hiển thị thông báo thành công
    showSuccessMessage(userInfo, productList, total);
  }

  // 👉 5. Hiển thị thông báo hoặc chuyển trang
  function showSuccessMessage(userInfo, productList, total) {

    // Lưu thông tin để hiển thị ở trang thankyou.html
const orderId = "OD" + Math.floor(Math.random() * 1000000);
localStorage.setItem("orderId", orderId);
localStorage.setItem("totalAmount", total.toLocaleString('en-US', { style: 'currency', currency: 'USD' }));

const firstName = document.getElementById("first-name").value.trim();
const lastName = document.getElementById("last-name").value.trim();
const fullName = `${firstName} ${lastName}`;

const address = document.getElementById("address").value.trim();
const city = document.getElementById("city").value.trim();
const state = document.getElementById("state").value.trim();
const fullAddress = `${address}, ${city}, ${state}`;

// Save to localStorage
localStorage.setItem("customerName", fullName);
localStorage.setItem("shippingAddress", fullAddress);

window.location.href = "thankyou.html";


    // (tuỳ chọn) redirect sang trang cảm ơn
     window.location.href = 'thankyou.html';
  }

  // Gán sự kiện cho nút "Order"
  document.querySelector('.order-button').addEventListener('click', handleOrder);

  // Cập nhật tổng ban đầu
  updateTotal();
