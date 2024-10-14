import { type RouteRecordRaw, createRouter, createWebHistory } from 'vue-router'
import Home from '@/presentation/screens/Home.vue'
import Hotel from '@/presentation/screens/Hotel.vue'
import Room from '@/presentation/screens/Room.vue'
import Location from '@/presentation/screens/Location.vue'
import Question from '@/presentation/screens/Question.vue'
import Inbox from '@/presentation/screens/Inbox.vue'
import Friends from '@/presentation/screens/Friends.vue'
import Profile from '@/presentation/screens/Profile.vue'
import Onboarding from '@/presentation/screens/Onboarding.vue'
import axios from 'axios'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    redirect: '/onboarding'
  },
  {
    path: '/start',
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
    path: '/home',
    component: Home,
  },
  {
    path: '/location',
    component: Location,
  },
  {
    path: '/hotel/:id',
    component: Hotel,
    props: route => ({
      id: parseInt(route.params.id as string, 10),
    }),
  },
  {
    path: '/room/:hotelId/:roomId',
    component: Room,
    props: route => ({
      hotelId: parseInt(route.params.hotelId as string, 10),
      roomId: parseInt(route.params.roomId as string, 10),
    }),
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
