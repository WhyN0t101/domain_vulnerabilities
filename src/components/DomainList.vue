<template>
    <div class="domain-list">
      <h1>Domain List</h1>
      <div v-if="domains && domains.length">
        <div 
          v-for="domain in domains" 
          :key="domain.domain" 
          class="domain-item"
        >
          <router-link :to="`/details/${domain.domain}`">
            <button class="domain-button">{{ domain.domain }}</button>
          </router-link>
        </div>
      </div>
      <p v-else>No domains available to display.</p>
    </div>
  </template>
  
  <script>
  export default {
    name: 'DomainList',
    props: ['domains'],
  };
  </script>
  
  <style scoped>
  .domain-list {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 15px;
    padding: 20px;
    max-width: 600px;
    width: 100%;
  }
  
  h1 {
    font-weight: 500;
    color: #333;
    margin-bottom: 15px;
  }
  
  .domain-item {
    width: 100%;
  }
  
  .domain-button {
    width: 100%;
    padding: 15px;
    font-size: 18px;
    font-weight: 500;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
    transition: all 0.3s;
  }
  
  .domain-button:hover {
    background-color: #0056b3;
    transform: scale(1.02);
  }
  </style>
  