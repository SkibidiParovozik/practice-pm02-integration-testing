import { createApp } from 'vue';
import { createRouter, createWebHistory } from 'vue-router';
import App from './App.vue';
import glavnoe from './glavnoe.vue';
import detali from './detali.vue';
import tovar from './tovar.vue';

const routes = [
  { path: '/', component: glavnoe },
  { path: '/catalog/category/:id', component: detali },
    { path: '/catalog/:type/:id', component: detali }, 
  { path: '/part/:id', component: tovar }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

const app = createApp(App);
app.use(router);
app.mount('#app');
