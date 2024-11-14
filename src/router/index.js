

import { createRouter, createWebHistory } from 'vue-router';
import DomainList from '../components/DomainList.vue';
import DomainDetails from '../components/DomainDetails.vue';
import domainData from '../domain.json'; // Import JSON data

const routes = [
  {
    path: '/',
    name: 'Home',
    component: DomainList,
  },
  {
    path: '/details/:domainName',
    name: 'Details',
    component: DomainDetails,
    props: route => ({
      domainData: domainData.find(
        domain => domain.domain === route.params.domainName
      ),
    }),
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
