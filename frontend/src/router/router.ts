import { type RouteRecordRaw, createRouter, createWebHistory } from 'vue-router'
import Question from '@/presentation/screens/Question.vue'
import Inbox from '@/presentation/screens/Inbox.vue'
import Friends from '@/presentation/screens/Friends.vue'
import Profile from '@/presentation/screens/Profile.vue'
import Onboarding from '@/presentation/screens/Onboarding.vue'
import useTelegram from '@/services/useTelegram'
// import { addFriend } from '@/infra/store/friends'

const { webAppInitData } = useTelegram()

// TODO: redirect to questions if user is already onboarded
const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: Onboarding,
    beforeEnter: async (to, from, next) => {
      try {
        const initData = new URLSearchParams(webAppInitData)
        const start_param = JSON.parse(initData.get('start_param') || '{}')
        if (start_param) {
          // await addFriend(Number(start_param))
        }
        next('/questions')
      } catch (error) {
        console.error('Error in / route:', error)
        next('/questions')
      }
    }
  },
  {
    path: '/onboarding',
    name: 'onboarding',
    // component: Onboarding
    component: Question
    // TODO: redirect to questions if user is already onboarded
  },
  {
    path: '/questions',
    name: 'questions',
    component: Question
  },
  // {
  //   path: '/inbox',
  //   name: 'inbox',
  //   component: Inbox
  // },
  // {
  //   path: '/friends',
  //   name: 'friends',
  //   // component: Friends
  //   component: Question
  // },
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
