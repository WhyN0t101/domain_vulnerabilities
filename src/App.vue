<template>
  <div id="app">
    <!-- Pass filtered domains to the DomainList component -->
    <router-view :domains="filteredDomains" />
  </div>
</template>

<script>
import domainData from './centro.json';

export default {
  name: 'App',
  data() {
    return {
      domains: Object.entries(domainData).map(([municipio, details]) => ({
        domain: details.sitio,
        municipio,
        rua: details.rua,
        codigopostal: details.codigopostal,
      })), // Convert object to array of domain objects
      searchQuery: '',
    };
  },
  computed: {
    filteredDomains() {
      return this.domains.filter(domain =>
        domain.domain.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    },
  },
};
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');

#app {
  font-family: 'Roboto', sans-serif;
  background-color: #f0f2f5;
  min-height: 100vh;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.search-bar {
  width: 100%;
  max-width: 600px;
  margin-bottom: 20px;
}

.search-bar input {
  width: 100%;
  padding: 12px 20px;
  border: 1px solid #ddd;
  border-radius: 25px;
  font-size: 16px;
  box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.1);
  outline: none;
  transition: box-shadow 0.2s;
}

.search-bar input:focus {
  box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.2);
}
</style>
