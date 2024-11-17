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
      <div v-if="filteredDomains && filteredDomains.length" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8">
        <div v-for="domain in filteredDomains" :key="domain.domain">
          <router-link :to="`/details/${domain.domain}`" class="block">
            <div class="bg-white rounded-xl shadow-lg hover:shadow-2xl transition-all duration-300 overflow-hidden border border-gray-100">
              <!-- Domain Card Header -->
              <div class="bg-gradient-to-r from-blue-500 to-indigo-600 p-6">
                <div class="flex items-center justify-between">
                  <div class="flex items-center space-x-3">
                    <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                            d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" />
                    </svg>
                    <h3 class="text-lg font-semibold text-white">{{ domain.domain }}</h3>
                  </div>
                </div>
              </div>

              <!-- Domain Card Body -->
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

                <div class="flex items-center space-x-3">
                  <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                  </svg>
                  <p class="text-sm text-gray-600">{{ domain.codigopostal || 'N/A' }}</p>
                </div>

                <!-- Action Button -->
                <button class="w-full mt-6 bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 
                             text-white font-medium py-3 px-4 rounded-lg transition-all duration-300 
                             flex items-center justify-center space-x-2 group">
                  <span>View Details</span>
                  <svg class="w-5 h-5 transform transition-transform group-hover:translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                  </svg>
                </button>
              </div>
            </div>
          </router-link>
        </div>
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
// Script Section (keeping things as they are)

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
