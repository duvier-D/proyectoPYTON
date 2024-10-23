<template>
  <div class="form-container">
    <div class="form-wrapper">
      <h1>Iniciar sesión</h1>
      <form @submit.prevent="loginUsuario">
        <div class="form-group">
          <label for="nombreUsuario">Nombre de Usuario:</label>
          <input type="number" id="nombreUsuario" v-model="nombreUsuario" required class="form-input" />
        </div>
        <div class="form-group">
          <label for="password">Contraseña:</label>
          <input type="password" id="password" v-model="password" required class="form-input" />
        </div>
        <button type="submit" class="form-submit-button">Iniciar sesión</button>
        <p v-if="menError" class="form-error">{{ menError }}</p>
        <p v-if="menExito" class="form-success">{{ menExito }}</p>
      </form>
    </div>
  </div>
</template>

<script setup>
import Swal from 'sweetalert2'
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()
const nombreUsuario = ref('')
const password = ref('')
const menError = ref('')
const menExito = ref('')

const loginUsuario = async () => {
  try {
    const response = await axios.post("http://127.0.0.1:8000/login", {
      nombre_usuario: nombreUsuario.value,
      password: password.value
    })

    const { rol: rolServidor } = response.data  // Obtener el rol

    // Verificamos el rol para depender del modulo
    if (rolServidor === "administrador") {
      router.push('/ModuloAdmin')
    } else if (["operario", "supervisor", "coordinador"].includes(rolServidor)) {
      router.push('/pesos')
    } else if (rolServidor === "usuario_epp") {
      router.push('/epps')
    } else {
      menError.value = "Rol no válido"
      Swal.fire({
        icon: 'error',
        title: 'Error',
        text: 'Rol no válido'
      });
      return
    }

    menExito.value = "Inicio de sesión exitoso"
    Swal.fire({
      icon: 'success',
      title: 'Inicio de Sesión',
      text: 'Inicio de sesión exitoso'
    });

  } catch (error) {
    console.error("Error al iniciar sesión", error)
    menError.value = "Error al iniciar sesión"
    Swal.fire({
      icon: 'error',
      title: 'Error',
      text: 'Error al iniciar sesión'
    })
  }
}
</script>

<style>
.form-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.form-wrapper {
  background-color: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 15px;
}

.form-input {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
}

.form-submit-button {
  background-color: #007bff;
  color: white;
  padding: 10px;
  border: none;
  cursor: pointer;
  width: 100%;
}

.form-error {
  color: red;
}

.form-success {
  color: green;
}
</style>
