import Vue from 'vue';
import Router from 'vue-router';
import Main from '@/components/Main';
import Confirm from '@/components/Confirm';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Main',
      component: Main,
    },
    {
      path: '/confirmpage',
      name: 'Confirm',
      component: Confirm,
    },
  ],
});
