import { type RouteRecordRaw, createRouter, createWebHistory } from 'vue-router'
import Question from '@/presentation/screens/Question.vue'
import Inbox from '@/presentation/screens/Inbox.vue'
import Friends from '@/presentation/screens/Friends.vue'
import Profile from '@/presentation/screens/Profile.vue'
import Onboarding from '@/presentation/screens/Onboarding.vue'
import { defineComponent } from 'vue'

// Add this dummy component
const DummyComponent = defineComponent({
  render: () => null
})

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    redirect: '/onboarding'
  },
  {
    path: '/start',
    component: DummyComponent,
    beforeEnter: async (to, from, next) => {
      try {
        // Send POST request to backend to /add_friend with friend as parameter from url parameters
        // TODO: implement
        // Redirect to onboarding
        next('/onboarding')
      } catch (error) {
        // TODO: implement proper error handling
        console.error('Error in /start route:', error)
        next('/onboarding')
      }
    }
  },
  {
    path: '/onboarding',
    name: 'onboarding',
    component: Onboarding
    // TODO: redirect to questions if user is already onboarded
  },
  {
    path: '/questions',
    name: 'questions',
    component: Question
  },
  {
    path: '/inbox',
    name: 'inbox',
    component: Inbox
  },
  {
    path: '/friends',
    name: 'friends',
    component: Friends
  },
  {
    path: '/profile',
    name: 'profile',
    component: Profile
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
