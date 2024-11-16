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
    props: { domainData }, // Pass domainData directly as a prop
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
