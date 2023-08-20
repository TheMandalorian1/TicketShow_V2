import { createRouter, createWebHistory } from 'vue-router'

import AdminLogin from '../components/AdminLogin.vue'
import SignUp from '../components/SignUp.vue'
import Login from '../components/Login.vue'
import AddVenue from '../components/AddVenue.vue'
import AddMovie from '../components/AddMovie.vue'
import AddShow from '../components/AddShow.vue'
import EditVenue from '../components/EditVenue.vue'
import EditMovie from '../components/EditMovie.vue'
import EditShow from '../components/EditShow.vue'
import RemoveMovie from '../components/RemoveMovie.vue'
import RemoveVenue from '../components/RemoveVenue.vue'
import RemoveShow from '../components/RemoveShow.vue'
import SearchResult from '../components/SearchResult.vue'
import UserDashboard from '../components/UserDashboard.vue'
import AdminDashboard from '../components/AdminDashboard.vue'
import RateMovie from '../components/RateMovie.vue'
import TicketBooking from '../components/TicketBooking.vue'
import BookedShow from '../components/BookedShow.vue'
import ExportVenue from '../components/ExportVenue.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // Admin routes
    {
      path: '/admin/login',
      name: 'AdminLogin',
      component: AdminLogin
    },
    {
      path: '/admin/dashboard',
      name: 'AdminDashboard',
      component: AdminDashboard
    },
    {
      path: '/addmovie',
      name: 'AddMovie',
      component: AddMovie
    },
    {
      path: '/addvenue',
      name: 'AddVenue',
      component: AddVenue
    },
    {
      path: '/addshow/:vid',
      name: 'AddShow',
      component: AddShow
    },
    {
      path: '/editmovie/:mid',
      name: 'EditMovie',
      component: EditMovie
    },
    {
      path: '/editvenue/:vid',
      name: 'EditVenue',
      component: EditVenue
    },
    {
      path: '/editshow/:sid',
      name: 'EditShow',
      component: EditShow
    },
    {
      path: '/deletemovie/:mid',
      name: 'RemoveMovie',
      component: RemoveMovie
    },
    {
      path: '/deletevenue/:vid',
      name: 'RemoveVenue',
      component: RemoveVenue
    },
    {
      path: '/deleteshow/:sid',
      name: 'RemoveShow',
      component: RemoveShow
    },
    {
      path: '/export',
      name: 'ExportVenue',
      component: ExportVenue
    },
    
    // User routes
    {
      path: '/login',
      name: 'Login',
      alias: '/',
      component: Login
    },
    {
      path: '/signup',
      name: 'SignUp',
      component: SignUp
    },
    {
      path: '/dashboard',
      name: 'UserDashboard',
      component: UserDashboard
    },
    {
      path: '/search',
      name: 'SearchResult',
      component: SearchResult
    },
    {
      path: '/rate',
      name: 'RateMovie',
      component: RateMovie
    },
    {
      path: '/book/:sid',
      name: 'TicketBooking',
      component: TicketBooking
    },
    {
      path: '/booked',
      name: 'BookedShow',
      component: BookedShow
    },
  ]
})

export default router
