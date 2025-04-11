// Lấy dữ liệu từ localStorage nếu có (truyền từ payment.js)
const orderId = localStorage.getItem("orderId") || "123456";
const totalAmount = localStorage.getItem("totalAmount") || "$XX.XX";

document.getElementById("order-id").textContent = orderId;
document.getElementById("order-total").textContent = totalAmount;
const customerName = localStorage.getItem("customerName") || "Customer";
const shippingAddress = localStorage.getItem("shippingAddress") || "your address";

document.getElementById("thank-you-message").textContent = 
  `Thank you, ${customerName}! Your order will be delivered to: ${shippingAddress}.`;