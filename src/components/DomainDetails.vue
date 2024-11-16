<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div v-if="domainDetails" class="max-w-4xl mx-auto px-4">
      <!-- Domain Header -->
      <div class="bg-white rounded-lg shadow-sm p-6 mb-6">
        <h1 class="text-3xl font-bold text-gray-900 mb-2">{{ domainDetails.domain }}</h1>
        <div class="h-1 w-20 bg-blue-500 rounded"></div>
      </div>

      <!-- Security Score Cards -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        <!-- DNSSEC Card -->
        <div class="bg-white rounded-lg shadow-sm p-6">
          <div class="flex items-center mb-4">
            <div class="p-2 bg-blue-100 rounded-lg">
              <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path>
              </svg>
            </div>
            <h2 class="text-xl font-semibold text-gray-900 ml-3">DNSSEC</h2>
          </div>
          
          <div class="space-y-3">
            <div class="flex items-center">
              <span class="font-medium text-gray-700">DNSSEC Valid:</span>
              <span :class="['ml-2 px-2 py-1 rounded text-sm', domainDetails.dnssec_tlsa.dnssec_valid ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800']">
                {{ domainDetails.dnssec_tlsa.dnssec_valid ? 'Yes' : 'No' }}
              </span>
            </div>
            
            <div v-if="domainDetails.dnssec_tlsa.error" class="text-red-600">
              {{ domainDetails.dnssec_tlsa.error }}
            </div>

            <div class="mt-4">
              <h3 class="text-sm font-semibold text-gray-700 mb-2">TLSA Records</h3>
              <ul class="space-y-2 text-sm text-gray-600">
                <li v-if="domainDetails.dnssec_tlsa.tlsa_records.length === 0" class="italic">No TLSA records found</li>
                <li v-for="(tlsa, index) in domainDetails.dnssec_tlsa.tlsa_records" 
                    :key="index"
                    class="bg-gray-50 p-2 rounded">
                  {{ tlsa }}
                </li>
              </ul>
            </div>
          </div>
        </div>

        <!-- Email Security Card -->
        <div class="bg-white rounded-lg shadow-sm p-6">
          <div class="flex items-center mb-4">
            <div class="p-2 bg-purple-100 rounded-lg">
              <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
              </svg>
            </div>
            <h2 class="text-xl font-semibold text-gray-900 ml-3">Email Security</h2>
          </div>

          <div class="space-y-3">
            <div v-if="domainDetails.email_security.error" class="text-red-600">
              {{ domainDetails.email_security.error }}
            </div>

            <div class="grid grid-cols-2 gap-4">
              <div class="col-span-2">
                <span class="text-sm font-medium text-gray-700">SPF Record:</span>
                <p class="mt-1 text-sm text-gray-600 bg-gray-50 p-2 rounded">
                  {{ domainDetails.email_security.spf_record || 'No SPF record found' }}
                </p>
              </div>

              <div class="col-span-2">
                <span class="text-sm font-medium text-gray-700">DMARC Record:</span>
                <p class="mt-1 text-sm text-gray-600 bg-gray-50 p-2 rounded">
                  {{ domainDetails.email_security.dmarc_record || 'No DMARC record found' }}
                </p>
              </div>

              <div class="flex items-center">
                <span class="text-sm font-medium text-gray-700">DKIM:</span>
                <span :class="['ml-2 px-2 py-1 rounded text-sm', domainDetails.email_security.dkim_supported ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800']">
                  {{ domainDetails.email_security.dkim_supported ? 'Supported' : 'Not Supported' }}
                </span>
              </div>

              <div class="flex items-center">
                <span class="text-sm font-medium text-gray-700">STARTTLS:</span>
                <span :class="['ml-2 px-2 py-1 rounded text-sm', domainDetails.email_security.starttls_supported ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800']">
                  {{ domainDetails.email_security.starttls_supported ? 'Supported' : 'Not Supported' }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- HTTPS & SSL/TLS Card -->
        <div class="bg-white rounded-lg shadow-sm p-6">
          <div class="flex items-center mb-4">
            <div class="p-2 bg-green-100 rounded-lg">
              <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path>
              </svg>
            </div>
            <h2 class="text-xl font-semibold text-gray-900 ml-3">HTTPS/SSL/TLS</h2>
          </div>

          <div class="space-y-3">
            <div v-if="domainDetails.https.error" class="text-red-600">
              {{ domainDetails.https.error }}
            </div>

            <div class="grid grid-cols-2 gap-4">
              <div class="flex items-center">
                <span class="text-sm font-medium text-gray-700">HTTPS Redirect:</span>
                <span :class="['ml-2 px-2 py-1 rounded text-sm', domainDetails.https.redirects_to_https ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800']">
                  {{ domainDetails.https.redirects_to_https ? 'Yes' : 'No' }}
                </span>
              </div>

              <div class="flex items-center">
                <span class="text-sm font-medium text-gray-700">HSTS:</span>
                <span :class="['ml-2 px-2 py-1 rounded text-sm', domainDetails.https.hsts_supported ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800']">
                  {{ domainDetails.https.hsts_supported ? 'Supported' : 'Not Supported' }}
                </span>
              </div>
            </div>

            <div class="mt-4">
              <h3 class="text-sm font-semibold text-gray-700 mb-2">SSL/TLS Versions</h3>
              <div class="flex flex-wrap gap-2">
                <span v-if="domainDetails.https.ssl_versions_supported.length === 0" class="text-sm text-gray-500 italic">
                  No SSL/TLS versions supported
                </span>
                <span v-for="(version, index) in domainDetails.https.ssl_versions_supported" 
                      :key="index"
                      class="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-sm">
                  {{ version }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- HTTP Security Headers Card -->
        <div class="bg-white rounded-lg shadow-sm p-6">
          <div class="flex items-center mb-4">
            <div class="p-2 bg-yellow-100 rounded-lg">
              <svg class="w-6 h-6 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path>
              </svg>
            </div>
            <h2 class="text-xl font-semibold text-gray-900 ml-3">Security Headers</h2>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div v-for="(value, key) in domainDetails.http_security_headers" 
                 :key="key" 
                 class="flex items-center">
              <span class="text-sm font-medium text-gray-700">{{ formatHeaderName(key) }}:</span>
              <span :class="['ml-2 px-2 py-1 rounded text-sm', value ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800']">
                {{ value ? 'Enabled' : 'Disabled' }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="flex justify-center items-center min-h-screen">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'DomainDetails',
  data() {
    return {
      domainDetails: null,
    };
  },
  created() {
    const domainName = this.$route.params.domainName;
    this.fetchDomainDetails(domainName);
  },
  methods: {
    async fetchDomainDetails(domainName) {
      try {
        const response = await axios.get(`http://192.168.209.129:5000/check_domain/${domainName}`);
        this.domainDetails = response.data;
      } catch (error) {
        console.error('Error fetching domain details:', error);
        this.domainDetails = { error: 'Failed to load domain details' };
      }
    },
    formatHeaderName(key) {
      return key
        .split('_')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ');
    }
  }
};
</script>