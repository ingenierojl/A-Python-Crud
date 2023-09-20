import { authFetch } from './auth.js';
export function login(username, password) {
  let token;
  const data = {username, password};

  console.log("antes del fetch");

  fetch('/login', {
    method: 'POST',
    body: new URLSearchParams(data) 
  })
  .then(response => {

    console.log("Response recibida"); 
    console.log(response);

    return response.json();
    

  })
  .then(data => {

    console.log("Token", data.access_token);
    const token = data.access_token; 

    // Guardar token
    localStorage.setItem('token', token);

    // Leer token
    const storedToken = localStorage.getItem('token');
    console.log("Token desde LocalStorage:", storedToken);

    // Llamar función para request autenticada
    authFetch('/protected');

  });

}