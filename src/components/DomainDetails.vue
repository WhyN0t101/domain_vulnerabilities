<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 py-8 px-4">
    <div v-if="domainDetails" class="max-w-5xl mx-auto space-y-6">
      <!-- Domain Header -->
      <header class="bg-white rounded-xl shadow-lg p-8 transform hover:scale-[1.02] transition-transform">
  <div class="flex items-center justify-between">
    <div class="flex items-center space-x-4">
      <div class="p-3 bg-blue-50 rounded-lg">
        <svg class="w-8 h-8 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" />
        </svg>
      </div>
      <div>
        <h1 class="text-3xl font-bold text-gray-900">{{ domainDetails.domain }}</h1>
        <p class="text-gray-500">Security Analysis Dashboard</p>
      </div>
    </div>
    <!-- Group the buttons together -->
    <div class="flex space-x-4">
      <button
        @click="generatePDF"
        class="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 focus:outline-none no-print"
      >
        Download Report
      </button>
      <button
        @click="goBack"
        class="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 focus:outline-none no-print"
      >
        Back
      </button>
    </div>
  </div>
</header>



      <!-- Security Status Card -->
      <div :class="[
        'rounded-xl p-6 shadow-lg transition-all duration-300',
        isVulnerable ? 'bg-red-50 border-l-4 border-red-500' : 'bg-green-50 border-l-4 border-green-500'
      ]">
        <div class="flex items-center">
          <div :class="[
            'p-3 rounded-full mr-4',
            isVulnerable ? 'bg-red-100' : 'bg-green-100'
          ]">
            <svg class="w-6 h-6" :class="isVulnerable ? 'text-red-500' : 'text-green-500'" fill="none"
              stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
          </div>
          <div>
            <h2 class="text-xl font-semibold" :class="isVulnerable ? 'text-red-800' : 'text-green-800'">
              Security Status
            </h2>
            <p class="text-sm mt-1" :class="isVulnerable ? 'text-red-600' : 'text-green-600'">
              {{ isVulnerable ? 'Vulnerabilities Detected' : 'No Critical Issues Found' }}
            </p>
          </div>
        </div>
      </div>

      <!-- Security Sections Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- DNSSEC Section -->
        <div class="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow">
          <div class="flex items-center mb-4">
            <div class="p-2 rounded-lg" :class="domainDetails.dnssec_tlsa.dnssec_valid ? 'bg-green-100' : 'bg-red-100'">
              <svg class="w-6 h-6" :class="domainDetails.dnssec_tlsa.dnssec_valid ? 'text-green-600' : 'text-red-600'"
                fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
            </div>
            <h3 class="ml-3 text-xl font-semibold">DNSSEC</h3>
          </div>

          <div class="space-y-3">
            <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <span class="font-medium">Status:</span>
              <span :class="[
                'px-3 py-1 rounded-full text-sm font-medium',
                domainDetails.dnssec_tlsa.dnssec_valid ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'
              ]">
                {{ domainDetails.dnssec_tlsa.dnssec_valid ? 'Valid' : 'Invalid' }}
              </span>
            </div>

            <div v-if="domainDetails.dnssec_tlsa.tlsa_records.length > 0">
              <p class="text-sm font-medium text-gray-700 mb-2">TLSA Records:</p>
              <div class="space-y-2">
                <div v-for="(tlsa, index) in domainDetails.dnssec_tlsa.tlsa_records" :key="index"
                  class="text-xs bg-gray-50 p-3 rounded-lg font-mono break-all">
                  {{ tlsa }}
                </div>
              </div>
            </div>

            <div v-if="domainDetails.dnssec_tlsa.recommendations.length > 0">
              <p class="text-sm font-medium text-red-700">Recommendations:</p>
              <ul class="list-disc list-inside">
                <li v-for="rec in domainDetails.dnssec_tlsa.recommendations" :key="rec" class="text-sm text-red-600">
                  {{ rec }}
                </li>
              </ul>
            </div>
          </div>
        </div>

        <!-- SSL Information Section -->
        <div class="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow">
          <div class="flex items-center mb-4">
            <div class="p-2 bg-purple-100 rounded-lg">
              <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
            </div>
            <h3 class="ml-3 text-xl font-semibold">SSL Information</h3>
          </div>

          <div class="space-y-4">
            <div class="grid grid-cols-2 gap-4">
              <div class="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                <span class="text-sm font-medium">Certificate Valid</span>
                <span :class="[
                  'px-3 py-1 rounded-full text-sm font-medium',
                  domainDetails.ssl_info.certificate_valid ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'
                ]">
                  {{ domainDetails.ssl_info.certificate_valid ? 'Yes' : 'No' }}
                </span>
              </div>

              <div class="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                <span class="text-sm font-medium">Issuer</span>
                <span class="text-sm text-gray-700">
                  {{ domainDetails.ssl_info.certificate_issuer || 'Unknown' }}
                </span>
              </div>
            </div>

            <div>
              <p class="text-sm font-medium">Certificate Chain:</p>
              <ul class="list-disc list-inside">
                <li v-for="chain in domainDetails.ssl_info.certificate_chain" :key="chain"
                  class="text-sm text-gray-700">
                  {{ chain }}
                </li>
              </ul>
            </div>

            <div>
              <p class="text-sm font-medium">Expiration Date:</p>
              <span class="text-sm text-gray-700">
                {{ domainDetails.ssl_info.certificate_expiration || 'Unknown' }}
              </span>
            </div>
          </div>
        </div>

        <!-- HTTP Security Headers Section -->
        <div class="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow">
          <div class="flex items-center mb-4">
            <div class="p-2 bg-amber-100 rounded-lg">
              <svg class="w-6 h-6 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            <h3 class="ml-3 text-xl font-semibold">HTTP Security Headers</h3>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div v-for="[header, value] in filteredHttpHeaders" :key="header"
              class="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
              <span class="text-sm font-medium capitalize">{{ header.replace('_', ' ') }}</span>
              <span :class="[
                'px-3 py-1 rounded-full text-sm font-medium',
                value ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'
              ]">
                {{ value ? 'Yes' : 'No' }}
              </span>
            </div>
          </div>

          <div v-if="domainDetails.http_headers.recommendations.length > 0">
            <p class="text-sm font-medium text-red-700">Recommendations:</p>
            <ul class="list-disc list-inside">
              <li v-for="rec in domainDetails.http_headers.recommendations" :key="rec" class="text-sm text-red-600">
                {{ rec }}
              </li>
            </ul>
          </div>
        </div>
      </div>

      <!-- Recommendations Section -->
      <div class="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow">
        <div class="flex items-center mb-4">
          <div class="p-2 bg-teal-100 rounded-lg">
            <svg class="w-6 h-6 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h10a2 2 0 012 2v14a2 2 0 01-2 2z" />
            </svg>
          </div>
          <h3 class="ml-3 text-xl font-semibold">Overall Recommendations</h3>
        </div>

        <div class="space-y-3">
          <p class="text-sm font-medium text-gray-700">Consolidated Recommendations:</p>
          <ul class="list-disc list-inside space-y-2">
            <li v-for="rec in allRecommendations" :key="rec" class="text-sm text-gray-800">
              {{ rec }}
            </li>
          </ul>
        </div>
      </div>

    </div>

    <!-- Loading Spinner -->
    <div v-else-if="loading" class="flex justify-center items-center h-screen">
      <div class="loader"></div>
    </div>

    <!-- Error Message -->
    <div v-if="error" class="flex justify-center items-center h-screen">
      <p class="text-lg text-red-600">{{ error }}</p>
    </div>
  </div>
</template>
<script>
import jsPDF from "jspdf";
import html2canvas from "html2canvas";

export default {
  data() {
    return {
      domainDetails: null,
      loading: true,
      error: null,
    };
  },
  computed: {
    isVulnerable() {
      return this.domainDetails?.recommendations?.vulnerabilities?.length > 0;
    },
    filteredHttpHeaders() {
      if (!this.domainDetails?.http_headers) return [];
      return Object.entries(this.domainDetails.http_headers).filter(
        ([key]) => key !== 'recommendations' && key !== 'security_score'
      );
    },
    allRecommendations() {
      const recommendations = [];
      if (this.domainDetails?.recommendations?.dnssec) {
        recommendations.push(...this.domainDetails.recommendations.dnssec);
      }
      if (this.domainDetails?.recommendations?.http_headers) {
        recommendations.push(...this.domainDetails.recommendations.http_headers);
      }
      if (this.domainDetails?.recommendations?.vulnerabilities) {
        recommendations.push(...this.domainDetails.recommendations.vulnerabilities);
      }
      return recommendations;
    },
  },
  methods: {
    async fetchDomainDetails() {
      this.loading = true; // Set loading to true when the request starts
      this.error = null; // Clear any previous errors

      try {
        // Actual API call to fetch domain details
        const response = await this.$axios.get(
          `${process.env.VUE_APP_API_BASE_URL}/check_domain/${this.$route.params.domain}`
        );

        if (response.status === 200) {
          this.domainDetails = response.data; // Set the data if the request is successful
        } else {
          throw new Error("Failed to fetch data: Non-200 response");
        }
      } catch (err) {
        // Error handling
        console.error("Error fetching domain details:", err);
        this.error =
          err.response?.data?.message || err.message || "Failed to load domain details."; // Display more detailed error if available
      } finally {
        this.loading = false; // Stop loading after the request completes (success or failure)
      }
    },
    goBack() {
      this.$router.go(-1); // Go back to the previous page
    },
    async generatePDF() {
      try {
        // Select the container element
        const element = document.querySelector(".max-w-5xl"); // Adjust to your container's class

        // Use html2canvas to capture the container as an image
        const canvas = await html2canvas(element, { scale: 2 });
        const imgData = canvas.toDataURL("image/png");

        // Initialize jsPDF
        const pdf = new jsPDF("p", "mm", "a4");
        const pdfWidth = pdf.internal.pageSize.getWidth();
        const pdfHeight = (canvas.height * pdfWidth) / canvas.width;

        // Add the image to the PDF
        pdf.addImage(imgData, "PNG", 0, 0, pdfWidth, pdfHeight);

        // Save the PDF file
        pdf.save(`${this.domainDetails.domain}-report.pdf`);
      } catch (error) {
        console.error("Error generating PDF:", error);
        alert("Failed to generate PDF. Please try again.");
      }
    },
  },
  created() {
    this.fetchDomainDetails(); // Fetch domain details when the component is created
  },
};
</script>
