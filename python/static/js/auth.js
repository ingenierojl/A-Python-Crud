export async function authFetch(url) {

    const token = localStorage.getItem('token');
  
    const options = {
      method: 'POST', 
      headers: {
        'Authorization': `Bearer ${token}`
      }
    };
    console.log(options);
    try {
  
      const response = await fetch(url, options);
  
      if(response.ok) {
        // Petición exitosa
        alert("Tienes acceso autorizado");  
      } else {
        // Hubo error
        alert("No tienes acceso. Debes iniciar sesión");  
      }
  
    } catch(error) {
      console.error(error);
    }
  
  }