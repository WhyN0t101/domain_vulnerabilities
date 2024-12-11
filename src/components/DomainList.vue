<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50 py-12 px-4">
    <div class="max-w-7xl mx-auto">
      <!-- Header Section -->
      <div class="text-center mb-16 animate-fade-in">
        <h1 class="text-5xl font-bold text-gray-900 mb-4">Municipalities Domain Directory</h1>
        <p class="text-lg text-gray-600 max-w-2xl mx-auto">Explore our comprehensive list of registered domains and their details.</p>
        <div class="h-1.5 w-32 bg-gradient-to-r from-blue-500 to-indigo-500 mx-auto rounded-full mt-6"></div>
      </div>

      <!-- Search Bar Section -->
      <div class="max-w-2xl mx-auto mb-12">
        <div class="relative">
          <span class="absolute inset-y-0 left-0 pl-4 flex items-center">
            <svg class="h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </span>
          <input
            type="text"
            v-model="searchQuery"
            placeholder="Search domains..."
            class="w-full pl-12 pr-4 py-3 rounded-xl border-2 border-gray-200 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all duration-300 outline-none bg-white/80 backdrop-blur-sm"
          />
        </div>
      </div>

      <!-- Domain Grid -->
      <div v-if="paginatedDomains.length" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8">
        <div v-for="domain in paginatedDomains" :key="domain.domain">
          <router-link :to="`/details/${domain.domain}`" class="block">
            <div class="bg-white rounded-xl shadow-lg hover:shadow-2xl transition-all duration-300 overflow-hidden border border-gray-100">
              <div class="bg-gradient-to-r from-blue-500 to-indigo-600 p-6">
                <h3 class="text-lg font-semibold text-white">{{ domain.domain }}</h3>
              </div>
              <div class="p-6 space-y-4">
                <div class="flex items-start space-x-3">
                  <svg class="w-5 h-5 text-gray-400 mt-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                  <div>
                    <p class="text-sm font-medium text-gray-900">{{ domain.municipio || 'N/A' }}</p>
                    <p class="text-sm text-gray-600">{{ domain.rua || 'N/A' }}</p>
                  </div>
                </div>
                <button class="w-full mt-6 bg-gradient-to-r from-blue-500 to-indigo-600 text-white py-3 px-4 rounded-lg">
                  View Details
                </button>
              </div>
            </div>
          </router-link>
        </div>
      </div>

      <div class="flex justify-center mt-12 space-x-2" v-if="totalPages > 1">
        <!-- Previous Button -->
        <button
          @click="goToPage(currentPage - 1)"
          :disabled="currentPage === 1"
          class="px-4 py-2 rounded-lg transition-all duration-200"
          :class="currentPage === 1 
            ? 'bg-gray-300 text-gray-500 cursor-not-allowed hover:bg-gray-400' 
            : 'bg-blue-100 text-blue-700 hover:bg-blue-200 hover:text-blue-900'"
        >
          Previous
        </button>

        <!-- Page Buttons -->
        <button
          v-for="page in visiblePages"
          :key="page"
          @click="goToPage(page)"
          class="px-4 py-2 rounded-lg transition-all duration-200"
          :class="currentPage === page 
            ? 'bg-blue-600 text-white hover:bg-blue-800' 
            : 'bg-gray-200 text-gray-700 hover:bg-blue-300 hover:text-gray-900'"
        >
          {{ page }}
        </button>

        <!-- Next Button -->
        <button
          @click="goToPage(currentPage + 1)"
          :disabled="currentPage === totalPages"
          class="px-4 py-2 rounded-lg transition-all duration-200"
          :class="currentPage === totalPages 
            ? 'bg-gray-300 text-gray-500 cursor-not-allowed hover:bg-gray-400' 
            : 'bg-blue-100 text-blue-700 hover:bg-blue-200 hover:text-blue-900'"
        >
          Next
        </button>
      </div>
      <!-- Empty State -->
      <div v-else class="text-center py-12">
        <p class="text-xl text-gray-600">No domains available to display</p>
        <p class="text-gray-500 mt-2">Try adjusting your search criteria</p>
      </div>
    </div>
  </div>
</template>


<script>
export default {
  name: 'DomainList',
  props: {
    domains: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      searchQuery: '', // Holds the search query input by the user
      currentPage: 1, // Current page number
      itemsPerPage: 20, // Number of items per page
    };
  },
  computed: {
    filteredDomains() {
      return this.domains.filter(domain =>
        domain.domain.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    },
    paginatedDomains() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.filteredDomains.slice(start, end);
    },
    totalPages() {
      return Math.ceil(this.filteredDomains.length / this.itemsPerPage);
    },
    visiblePages() {
      const totalVisible = 5; // Number of pages to show in the pagination bar
      const half = Math.floor(totalVisible / 2);
      let start = Math.max(this.currentPage - half, 1);
      let end = Math.min(start + totalVisible - 1, this.totalPages);

      // Adjust start if we're at the end
      if (end - start + 1 < totalVisible) {
        start = Math.max(end - totalVisible + 1, 1);
      }

      return Array.from({ length: end - start + 1 }, (_, i) => start + i);
    },
  },
  methods: {
    goToPage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page;
      }
    },
  },
};
</script>


<style scoped>
/* Basic Animation */
@keyframes fade-in {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

/* Optimizing for layout stability */
.animate-fade-in-up {
  animation: fade-in 0.6s ease-out forwards;
}

/* Preload external resources */
@import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@300;400;600&display=swap');

/* Efficient CSS/JS */
body {
  font-family: 'Open Sans', sans-serif;
}
</style>
