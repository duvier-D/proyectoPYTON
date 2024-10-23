<template>
    <div class="admin-section">
      <h2>Registrar Pesos</h2>
      <div class="content-container">
        <div class="form-wrapper">
          <form @submit.prevent="agregarRegistro">
            <div class="form-group">
              <label for="documento">Documento del Empleado:</label>
              <input type="number" v-model="nuevoRegistro.empleado_documento" required class="form-input"/>
            </div>
            <div class="form-group">
              <label for="tipo">Tipo de Registro:</label>
              <select v-model="nuevoRegistro.tipo" required class="form-input">
                <option value="patologico">Patológico</option>
                <option value="biosanitario">Biosanitario</option>
              </select>
            </div>
            <div class="form-group">
              <label for="peso">Peso (kg):</label>
              <input type="number" step="0.01" v-model="nuevoRegistro.peso" required class="form-input"/>
            </div>
            <div class="form-group">
              <label for="fecha">Fecha:</label>
              <input type="date" v-model="nuevoRegistro.fecha" required class="form-input"/>
            </div>
            <div class="form-group">
              <label for="hora">Hora:</label>
              <input type="time" v-model="nuevoRegistro.hora" required class="form-input"/>
            </div>
            <div class="cont-btn">
              <button type="submit" class="form-submit-button">Registrar Peso</button>
            </div>
          </form>
        </div>
  
        <h3>Lista de Registros</h3>
        <div class="table-container">
          <table>
            <thead>
              <tr>
                <th>Empleado Documento</th>
                <th>Peso (kg)</th>
                <th>Tipo</th>
                <th>Fecha</th>
                <th>Hora</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="registro in registros" :key="registro.id_registro"> <!-- Cambia aquí el key -->
                <td>{{ registro.empleado_documento }}</td>
                <td>{{ registro.peso }} kg</td>
                <td>{{ registro.tipo }}</td>
                <td>{{ registro.fecha }}</td>
                <td>{{ registro.hora }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import axios from 'axios';
  
  const nuevoRegistro = ref({
    empleado_documento: '',
    tipo: 'patologico',
    peso: '',
    fecha: '',
    hora: '',
  });
  
  const registros = ref([]);
  
  const agregarRegistro = async () => {
    try {
      const response = await axios.post('http://localhost:8000/insertarpesos', nuevoRegistro.value);
      registros.value.push(response.data);
      nuevoRegistro.value = {
        empleado_documento: '',
        tipo: 'patologico',
        peso: '',
        fecha: '',
        hora: '',
      };
    } catch (error) {
      console.error('Error al agregar el registro:', error);
    }
  };
  
  const obtenerRegistros = async () => {
    try {
      const response = await axios.get('http://localhost:8000/consultarpesos');
      registros.value = response.data;
    } catch (error) {
      console.error('Error al obtener los registros:', error);
    }
  };
  
  onMounted(() => {
    obtenerRegistros();
  });
  </script>
  
  <style scoped>
  .admin-section {
    padding: 20px;
  }
  
  .content-container {
    display: flex;
    flex-direction: column;
  }
  
  .form-wrapper {
    margin-bottom: 20px;
  }
  
  .form-group {
    margin-bottom: 15px;
  }
  
  .form-input {
    width: 100%;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
    margin-top: 5px;
  }
  
  .cont-btn {
    display: flex;
    justify-content: space-between;
  }
  
  .form-submit-button {
    background-color: #4CAF50;
    color: white;
    width: 100%;
    border: none;
    padding: 10px;
    cursor: pointer;
    border-radius: 4px;
  }
  
  .table-container {
    width: 100%;
    margin-top: 20px;
  }
  
  table {
    width: 100%;
    background-color: antiquewhite;
    border-collapse: collapse;
  }
  
  th, td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: left;
  }
  
  th {
    background-color: #f2f2f2;
  }
  </style>
  