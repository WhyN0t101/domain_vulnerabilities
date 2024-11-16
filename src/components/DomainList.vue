<template>
  <div class="min-h-screen bg-gray-50 py-8 px-4">
    <div class="max-w-7xl mx-auto">
      <!-- Header Section -->
      <div class="text-center mb-12">
        <h1 class="text-4xl font-bold text-gray-900 mb-4">Domain List</h1>
        <div class="h-1 w-24 bg-blue-500 mx-auto rounded"></div>
      </div>

      <!-- Domain Grid -->
      <div v-if="domains && domains.length" 
           class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        <div v-for="domain in domains" 
             :key="domain.domain" 
             class="transform transition-all duration-300 hover:scale-105">
          <router-link :to="`/details/${domain.domain}`" class="block">
            <div class="bg-white rounded-lg shadow-md hover:shadow-xl transition-shadow duration-300 overflow-hidden">
              <!-- Domain Card Header -->
              <div class="bg-gradient-to-r from-blue-500 to-blue-600 p-4">
                <div class="flex items-center justify-between">
                  <div class="flex items-center space-x-2">
                    <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                            d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" />
                    </svg>
                  </div>
                </div>
              </div>
              
              <!-- Domain Card Body -->
              <div class="p-6">
                <h2 class="text-xl font-semibold text-gray-800 mb-2">
                  {{ domain.municipio }}
                </h2>
                <p class="text-sm text-gray-600 mb-4">
                  {{ domain.domain }}
                </p>
                
                <!-- Action Button -->
                <button class="w-full bg-blue-500 hover:bg-blue-600 text-white font-medium py-3 px-4 rounded-lg
                             transition-colors duration-300 flex items-center justify-center space-x-2">
                  <span>View Details</span>
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                          d="M9 5l7 7-7 7" />
                  </svg>
                </button>
              </div>
            </div>
          </router-link>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else class="text-center py-12">
        <div class="bg-white rounded-lg shadow-md p-8 max-w-md mx-auto">
          <svg class="w-16 h-16 text-gray-400 mb-4 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                  d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <p class="text-xl text-gray-600">No domains available to display.</p>
        </div>
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
      default: () => [],
    }
  }
};
</script>