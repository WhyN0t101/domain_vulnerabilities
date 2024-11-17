import { createRouter, createWebHistory } from 'vue-router';
import DomainList from '../components/DomainList.vue';
import DomainDetails from '../components/DomainDetails.vue';

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
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
