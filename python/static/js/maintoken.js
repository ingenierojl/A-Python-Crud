import { login } from './token.js';
const form = document.getElementById('loginForm');

form.addEventListener('submit', event => {

  event.preventDefault();

  const username = form.username.value;
  const password = form.password.value;
  
  login(username, password); // Llamar a la función login
  
});