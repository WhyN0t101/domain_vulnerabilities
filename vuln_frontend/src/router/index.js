import { createRouter, createWebHistory } from 'vue-router';
import DomainList from '../components/DomainList.vue';
import DomainDetails from '../components/DomainDetails.vue';

const routes = [
  { path: '/', component: DomainList, name: 'Home' },
  { path: '/details/:domain', component: DomainDetails, name: 'DomainDetails' },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
