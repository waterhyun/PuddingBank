// stores/auth.js
import { defineStore } from 'pinia'
import axios from 'axios'

const API_URL = 'http://127.0.0.1:8000/api/v1'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: sessionStorage.getItem('token') || null,
    user: JSON.parse(sessionStorage.getItem('user')) || null,
    isLoading: false,
    error: null
  }),

  getters: {
    // isAuthenticated를 computed 속성으로 정의
    isAuthenticated: (state) => {
      return !!state.token && !!state.user
    }
  },

  actions: {
    async login(credentials) {
      try {
        this.isLoading = true
        this.error = null
        
        const response = await axios.post(`${API_URL}/accounts/login/`, {
          username: credentials.username,
          password: credentials.password
        })

        this.token = response.data.key
        sessionStorage.setItem('token', response.data.key)
        axios.defaults.headers.common['Authorization'] = `Token ${response.data.key}`
        
        await this.fetchUserDetails()
        return response
      } catch (error) {
        this.error = error.response?.data?.non_field_errors?.[0] || '로그인에 실패했습니다.'
        throw error
      } finally {
        this.isLoading = false
      }
    },

    async signup(userData) {
      try {
        this.isLoading = true
        this.error = null
        
        const response = await axios.post(`${API_URL}/accounts/signup/`, {
          username: userData.username,
          email: userData.email,
          password1: userData.password1,
          password2: userData.password2,
          name: userData.name,
          birthdate: userData.birthdate,
          phone: userData.phone || ''
        })
        return response
      } catch (error) {
        this.error = error.response?.data || '회원가입에 실패했습니다.'
        throw error
      } finally {
        this.isLoading = false
      }
    },

    async logout() {
      try {
        this.isLoading = true
        this.error = null
        
        if (this.token) {
          await axios.post(`${API_URL}/accounts/logout/`, {}, {
            headers: {
              'Authorization': `Token ${this.token}`
            }
          })
        }
      } catch (error) {
        console.error('Logout error:', error)
      } finally {
        this.token = null
        this.user = null
        sessionStorage.removeItem('token')
        sessionStorage.removeItem('user')
        delete axios.defaults.headers.common['Authorization']
        this.isLoading = false
      }
    },

    async fetchUserDetails() {
      try {
        const response = await axios.get(`${API_URL}/accounts/user/`, {
          headers: {
            'Authorization': `Token ${this.token}`
          }
        })
        this.user = response.data
        sessionStorage.setItem('user', JSON.stringify(response.data))
        return response.data
      } catch (error) {
        throw error
      }
    },

    async updateProfile(userData) {
      try {
        const response = await axios.put(`${API_URL}/accounts/profile/update/`, userData, {
          headers: {
            'Authorization': `Token ${this.token}`
          }
        })
        this.user = response.data
        sessionStorage.setItem('user', JSON.stringify(response.data))
        return response.data
      } catch (error) {
        throw error
      }
    },

    
    async changePassword(passwordData) {
      try {
        const response = await axios.post(`${API_URL}/accounts/password/change/`, {
          old_password: passwordData.old_password,
          new_password1: passwordData.new_password1,
          new_password2: passwordData.new_password2
        }, {
          headers: {
            'Authorization': `Token ${this.token}`
          }
        })
        return response
      } catch (error) {
        throw error
      }
    }
  }
})