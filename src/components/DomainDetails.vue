<template>
  <div class="domain-details" v-if="domainData">
    <h2>Details for {{ domainData.domain }}</h2>
    <div class="details-section">
      <h3>SSL Info</h3>
      <pre>{{ domainData.ssl_info }}</pre>
    </div>
    <div class="details-section">
      <h3>TLS Info</h3>
      <pre>{{ domainData.tls_info }}</pre>
    </div>
    <div class="details-section">
      <h3>DNSSEC</h3>
      <pre>{{ domainData.dnssec }}</pre>
    </div>
    <div class="details-section">
      <h3>Vulnerabilities</h3>
      <pre>{{ domainData.vulnerabilities }}</pre>
    </div>
  </div>

  <p v-else>Loading domain details...</p> <!-- Show a message while loading -->
</template>

<script>
export default {
  props: {
    domainData: {
      type: Object,
      required: true,
    },
  },
  methods: {
    goBack() {
      this.$emit('back-to-list');
    },
  },
};
</script>


<style scoped>
.domain-details {
  padding: 20px;
  max-width: 800px;
  width: 100%;
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
  margin: 0 auto;
}

h2 {
  color: #333;
  font-weight: 500;
  margin-bottom: 20px;
}

.details-section {
  margin-bottom: 20px;
}

.back-button {
  background-color: #007bff;
  color: white;
  padding: 10px 20px;
  font-size: 16px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
  display: block;
  margin: 0 auto;
}

.back-button:hover {
  background-color: #0056b3;
}
</style>
