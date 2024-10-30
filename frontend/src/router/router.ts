import { type RouteRecordRaw, createRouter, createWebHistory } from 'vue-router';
import Question from '@/presentation/screens/Question.vue';
import Inbox from '@/presentation/screens/Inbox.vue';
import Friends from '@/presentation/screens/Friends.vue';
import Profile from '@/presentation/screens/Profile.vue';
import Onboarding from '@/presentation/screens/Onboarding.vue';
import { useUserStore } from '@/store/user';
import { useInviterStore } from '@/store/inviter';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    redirect: '/questions',
  },
  {
    path: '/onboarding',
    name: 'onboarding',
    component: Onboarding,
  },
  {
    path: '/inviter',
    name: 'inviter',
    component: () => import('@/presentation/screens/Inviter.vue'),
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
    const userStore = useUserStore();
    const inviterStore = useInviterStore();
    const inviter = inviterStore.getInviter;

    // Forcing onboarding if user is not onboarded
    // Forcing inviter after onboarding
    if (!userStore.user?.is_onboarded) {
      if (to.name !== 'onboarding') {
        console.log('redirecting to onboarding');
        return next('/onboarding');
      }
    } else if (inviter) {
      if (to.name !== 'inviter') {
        console.log('redirecting to inviter');
        return next('/inviter');
      }
    }

    next();
  } catch (error) {
    console.error('Navigation guard error:', error);
    next();
  }
});

export default router;
