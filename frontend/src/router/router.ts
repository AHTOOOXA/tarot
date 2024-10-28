import { type RouteRecordRaw, createRouter, createWebHistory } from 'vue-router';
import Question from '@/presentation/screens/Question.vue';
import Inbox from '@/presentation/screens/Inbox.vue';
import Friends from '@/presentation/screens/Friends.vue';
import Profile from '@/presentation/screens/Profile.vue';
import Onboarding from '@/presentation/screens/Onboarding.vue';
import { useUserStore } from '@/store/user';
import { processStart } from '@/composables/start';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    redirect: '/onboarding',
  },
  {
    path: '/onboarding',
    name: 'onboarding',
    component: Onboarding,
    beforeEnter: async (to, from, next) => {
      try {
        const userStore = useUserStore();
        const user = userStore.user;

        if (user?.is_onboarded) {
          next('/questions');
        } else {
          next();
        }
      } catch (error) {
        console.error('Error in /onboarding route:', error);
        next();
      }
    },
  },
  {
    path: '/questions',
    name: 'questions',
    component: Question,
  },
  {
    path: '/inbox',
    name: 'inbox',
    component: Inbox,
  },
  {
    path: '/friends',
    name: 'friends',
    component: Friends,
  },
  {
    path: '/profile',
    name: 'profile',
    component: Profile,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Global navigation guard that runs before any route
router.beforeEach(async (to, from, next) => {
  try {
    // Process start parameters only once when the app starts
    if (from.path === '/') {
      await processStart();
    }
    next();
  } catch (error) {
    console.error('Error processing start parameters:', error);
    next();
  }
});

export default router;
