import { defineStore } from 'pinia';
import api from '@/services/api';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    user: JSON.parse(localStorage.getItem('user')) || null,
  }),

  getters: {
    isLoggedIn: (state) => !!state.token,
    isAdmin: (state) => {
      return state.user && state.user.is_admin ? state.user.is_admin : false;
    },
  },

  actions: {
    async login(credentials) {
      try {
        const formData = new URLSearchParams();
        formData.append('username', credentials.username);
        formData.append('password', credentials.password);

        const response = await api.post('/api/v1/login/access-token', formData, {
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        });
        
        const token = response.data.access_token;
        this.setToken(token);
        await this.fetchUser();

      } catch (error) {
        this.logout(); // 실패 시 상태 초기화

        // ✅ 수정된 부분: 에러를 가공하여 다시 throw
        // 백엔드에서 보낸 구체적인 에러 메시지를 우선적으로 사용합니다.
        let message = "서버와 통신 중 오류가 발생했습니다.";
        if (error.response && error.response.data && error.response.data.detail) {
          message = error.response.data.detail;
        } else if (error.request) {
          message = "서버로부터 응답을 받지 못했습니다. 네트워크를 확인해주세요.";
        }
        // 가공된 에러 메시지를 포함하여 에러를 다시 던져서,
        // 컴포넌트의 catch 블록에서 상세 내용을 알 수 있도록 합니다.
        throw new Error(message);
      }
    },

    async fetchUser() {
        if (!this.token) return;
        try {
            const response = await api.post('/api/v1/login/test-token');
            this.setUser(response.data);
        } catch (error) {
            this.logout();
        }
    },

    logout() {
      this.token = null;
      this.user = null;
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      
      // ✅ 수정된 부분: api 객체와 하위 속성이 있는지 확인 후 헤더 삭제
      if (api && api.defaults && api.defaults.headers && api.defaults.headers.common) {
        delete api.defaults.headers.common['Authorization'];
      }
    },

    setToken(token) {
        this.token = token;
        localStorage.setItem('token', token);
        api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    },

    setUser(user) {
        this.user = user;
        localStorage.setItem('user', JSON.stringify(user));
    },

    async checkAuth() {
        if (this.token) {
            if (!api.defaults.headers.common['Authorization']) {
                api.defaults.headers.common['Authorization'] = `Bearer ${this.token}`;
            }
            await this.fetchUser();
        }
    }
  },
});

