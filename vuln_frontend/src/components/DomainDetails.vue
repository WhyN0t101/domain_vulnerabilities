<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 py-8 px-4 antialiased">
    <div v-if="domainDetails" class="max-w-6xl mx-auto space-y-8">
      <!-- Domain Header with Enhanced Layout -->
      <header class="bg-white rounded-2xl shadow-lg p-6 flex items-center justify-between hover:shadow-xl transition-all duration-300">
        <div class="flex items-center space-x-6">
          <div class="bg-blue-100 p-4 rounded-xl">
            <svg class="w-10 h-10 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" />
            </svg>
          </div>
          <div>
            <h1 class="text-4xl font-bold text-gray-900 tracking-tight">{{ domainDetails.domain }}</h1>
            <p class="text-gray-500 text-sm mt-1">Comprehensive Security Analysis</p>
          </div>
        </div>
        <div class="flex space-x-4">
          <button @click="generatePDF" class="btn-primary">
            Download Report
          </button>
          <button @click="goBack" class="btn-secondary">
            Back
          </button>
        </div>
      </header>

      <!-- Security Status with More Prominent Styling -->
      <div :class="[
        'rounded-2xl p-6 shadow-md transition-all duration-300 flex items-center space-x-6',
        isVulnerable 
          ? 'bg-red-50 border-l-8 border-red-500 hover:bg-red-100' 
          : 'bg-green-50 border-l-8 border-green-500 hover:bg-green-100'
      ]">
        <div :class="[
          'p-4 rounded-xl',
          isVulnerable ? 'bg-red-100' : 'bg-green-100'
        ]">
          <svg class="w-8 h-8" :class="isVulnerable ? 'text-red-500' : 'text-green-500'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
        </div>
        <div>
          <h2 class="text-2xl font-bold" :class="isVulnerable ? 'text-red-800' : 'text-green-800'">
            Security Status
          </h2>
          <p class="text-sm mt-1" :class="isVulnerable ? 'text-red-600' : 'text-green-600'">
            {{ isVulnerable ? 'Vulnerabilities Detected' : 'No Critical Issues Found' }}
          </p>
        </div>
      </div>

      <!-- Reorganized Security Sections -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
        <!-- DNSSEC Section -->
        <section class="security-card">
          <div class="card-header">
            <div class="icon-bg" :class="domainDetails.dnssec_tlsa.dnssec_valid ? 'bg-green-100' : 'bg-red-100'">
              <svg class="w-6 h-6" :class="domainDetails.dnssec_tlsa.dnssec_valid ? 'text-green-600' : 'text-red-600'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
            </div>
            <h3>DNSSEC</h3>
          </div>

          <div class="card-content">
            <div class="status-badge" :class="domainDetails.dnssec_tlsa.dnssec_valid ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'">
              Status: {{ domainDetails.dnssec_tlsa.dnssec_valid ? 'Valid' : 'Invalid' }}
            </div>

            <div v-if="domainDetails.dnssec_tlsa.recommendations.length" class="recommendations">
              <p class="text-red-700 font-semibold mb-2">Recommendations:</p>
              <ul>
                <li v-for="rec in domainDetails.dnssec_tlsa.recommendations" :key="rec" class="text-red-600">
                  {{ rec }}
                </li>
              </ul>
            </div>
          </div>
        </section>

        <!-- SSL Information Section -->
        <section class="security-card">
          <div class="card-header">
            <div class="icon-bg bg-purple-100">
              <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
            </div>
            <h3>SSL Information</h3>
          </div>

          <div class="card-content">
            <div class="grid grid-cols-2 gap-4">
              <div class="status-badge" :class="domainDetails.ssl_info.certificate_valid ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'">
                Certificate Valid: {{ domainDetails.ssl_info.certificate_valid ? 'Yes' : 'No' }}
              </div>
              <div class="status-badge bg-gray-100 text-gray-700">
                Issuer: {{ domainDetails.ssl_info.certificate_issuer || 'Unknown' }}
              </div>
            </div>
            <div class="mt-4">
              <p class="font-semibold mb-2">Expiration Date:</p>
              <p>{{ domainDetails.ssl_info.certificate_expiration || 'Unknown' }}</p>
            </div>
          </div>
        </section>
      </div>
          <!-- HTTP Security Headers Section -->
    <section class="security-card mt-8">
      <div class="card-header">
        <div class="icon-bg bg-amber-100">
          <svg class="w-6 h-6 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
        </div>
        <h3>HTTP Security Headers</h3>
      </div>

      <div class="card-content">
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div v-for="[header, value] in filteredHttpHeaders" :key="header" 
               class="flex justify-between items-center bg-gray-50 p-3 rounded-lg">
            <span class="text-sm font-medium capitalize">
              {{ header.replace('_', ' ') }}
            </span>
            <span :class="[
              'px-3 py-1 rounded-full text-sm font-medium',
              value ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'
            ]">
              {{ value ? 'Present' : 'Missing' }}
            </span>
          </div>
        </div>

        <div v-if="domainDetails.http_headers.recommendations.length" class="mt-6">
          <p class="text-red-700 font-semibold mb-2">Recommendations:</p>
          <ul class="space-y-2 list-disc list-inside">
            <li v-for="rec in domainDetails.http_headers.recommendations" :key="rec" 
                class="text-red-600">
              {{ rec }}
            </li>
          </ul>
        </div>
      </div>
    </section>
      <!-- Recommendations Section -->
      <section class="bg-white rounded-2xl shadow-lg p-8">
        <div class="flex items-center mb-6">
          <div class="p-3 bg-teal-100 rounded-xl mr-4">
            <svg class="w-7 h-7 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h10a2 2 0 012 2v14a2 2 0 01-2 2z" />
            </svg>
          </div>
          <h3 class="text-2xl font-bold text-gray-800">Overall Recommendations</h3>
        </div>

        <ul class="space-y-3">
          <li v-for="rec in allRecommendations" :key="rec" class="text-gray-700 flex items-start">
            <svg class="w-5 h-5 text-teal-500 mr-3 mt-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            {{ rec }}
          </li>
        </ul>
      </section>

      <!-- Vulnerabilities Section -->
      <section class="bg-white rounded-2xl shadow-lg p-8">
        <h3 class="text-2xl font-bold mb-6 text-gray-800">Vulnerabilities</h3>
        <div v-if="vulnerabilitiesList.length" class="space-y-4">
          <div v-for="vul in vulnerabilitiesList" :key="vul.id" class="bg-gray-50 p-4 rounded-lg border-l-4" 
               :class="severityColor(vul.severity)">
            <div class="flex justify-between items-center mb-2">
              <span class="font-semibold text-gray-700">Vulnerability ID: {{ vul.id }}</span>
              <span class="text-sm font-medium" :class="severityTextColor(vul.severity)">
                {{ vul.severity }}
              </span>
            </div>
            <p class="text-gray-600">{{ vul.description }}</p>
          </div>
        </div>
        <p v-else class="text-gray-500 text-center">No vulnerabilities detected.</p>
      </section>
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
      return Object.values(this.domainDetails?.vulnerabilities || {}).some((cat) => cat.cves.length > 0);
    },
    filteredHttpHeaders() {
      if (!this.domainDetails?.http_headers) return [];
      return Object.entries(this.domainDetails.http_headers).filter(
        ([key]) => key !== 'recommendations' && key !== 'security_score'
      );
    },
    allRecommendations() {
      return this.domainDetails?.recommendations?.all || [];
    },
    vulnerabilitiesList() {
      return Object.values(this.domainDetails?.vulnerabilities || {}).flatMap((cat) => cat.cves);
    },
  },
  methods: {
    severityColor(severity) {
      const colors = {
        'Critical': 'border-red-500',
        'High': 'border-orange-500',
        'Medium': 'border-yellow-500',
        'Low': 'border-green-500'
      };
      return colors[severity] || 'border-gray-300';
    },
    severityTextColor(severity) {
      const colors = {
        'Critical': 'text-red-600',
        'High': 'text-orange-600',
        'Medium': 'text-yellow-600',
        'Low': 'text-green-600'
      };
      return colors[severity] || 'text-gray-600';
    },
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
    const element = document.querySelector(".max-w-6xl"); // Select the container element
    const canvas = await html2canvas(element, {
      scale: 2, // High-resolution capture for clarity
      useCORS: true, // Enable cross-origin for external assets
    });

    const pdf = new jsPDF("p", "mm", "a4"); // A4 size in portrait
    const pdfWidth = pdf.internal.pageSize.getWidth();
    const pdfHeight = pdf.internal.pageSize.getHeight();

    const canvasWidth = canvas.width;
    const canvasHeight = canvas.height;

    // Calculate the scale ratio for fitting the content proportionally
    const scaleRatio = pdfWidth / canvasWidth;
    const scaledHeight = canvasHeight * scaleRatio;

    // Handle content spanning multiple pages
    let position = 0;
    while (position < scaledHeight) {
      const pageCanvas = document.createElement("canvas");
      pageCanvas.width = canvasWidth;
      pageCanvas.height = pdfHeight / scaleRatio;

      const ctx = pageCanvas.getContext("2d");
      ctx.drawImage(
        canvas,
        0,
        position / scaleRatio,
        canvasWidth,
        pageCanvas.height,
        0,
        0,
        canvasWidth,
        pageCanvas.height
      );

      const pageData = pageCanvas.toDataURL("image/png");
      pdf.addImage(pageData, "PNG", 0, 0, pdfWidth, pdfHeight);

      position += pdfHeight;
      if (position < scaledHeight) {
        pdf.addPage();
      }
    }

    pdf.save(`${this.domainDetails.domain}-report.pdf`);
  } catch (error) {
    console.error("Error generating PDF:", error.message);
    alert("Failed to generate PDF. Please try again.");
  }
}
,
  },
  created() {
    this.fetchDomainDetails(); // Fetch domain details when the component is created
  },
};
</script>
<style scoped>

.btn-primary {
  @apply bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors;
}

.btn-secondary {
  @apply bg-gray-200 text-gray-800 px-4 py-2 rounded-lg hover:bg-gray-300 transition-colors;
}

.security-card {
  @apply bg-white rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300;
}

.card-header {
  @apply flex items-center space-x-4 p-6 border-b border-gray-100;
}

.card-header .icon-bg {
  @apply p-3 rounded-xl;
}

.card-header h3 {
  @apply text-xl font-bold text-gray-800;
}

.card-content {
  @apply p-6 space-y-4;
}

.status-badge {
  @apply px-4 py-2 rounded-lg text-sm font-medium inline-block;
}

.recommendations ul {
  @apply space-y-2 list-disc list-inside;
}
</style>