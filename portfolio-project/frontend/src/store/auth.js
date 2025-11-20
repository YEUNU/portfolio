import { defineStore } from 'pinia';
import api from '@/services/api';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    user: JSON.parse(localStorage.getItem('user')) || null,
    tokenExpiresAt: localStorage.getItem('tokenExpiresAt')
      ? new Date(localStorage.getItem('tokenExpiresAt'))
      : null,
    warningTimer: null,
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

        const { access_token, expires_in } = response.data;
        this.setToken(access_token, expires_in);
        await this.fetchUser();
        this.startTokenManagement();
      } catch (error) {
        this.logout(); // 실패 시 상태 초기화

        // ✅ 수정된 부분: 에러를 가공하여 다시 throw
        // 백엔드에서 보낸 구체적인 에러 메시지를 우선적으로 사용합니다.
        let message = '서버와 통신 중 오류가 발생했습니다.';
        if (error.response && error.response.data && error.response.data.detail) {
          message = error.response.data.detail;
        } else if (error.request) {
          message = '서버로부터 응답을 받지 못했습니다. 네트워크를 확인해주세요.';
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
        // 토큰이 만료되었거나 유효하지 않음
        this.logout();
        throw error;
      }
    },

    async refreshToken() {
      try {
        const response = await api.post('/api/v1/login/refresh-token');
        const { access_token, expires_in } = response.data;
        this.setToken(access_token, expires_in);
        this.startTokenManagement();
        return true;
      } catch (error) {
        console.error('Token refresh failed:', error);
        this.logout();
        return false;
      }
    },

    logout() {
      this.clearTimer();
      this.token = null;
      this.user = null;
      this.tokenExpiresAt = null;
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      localStorage.removeItem('tokenExpiresAt');

      // ✅ 수정된 부분: api 객체와 하위 속성이 있는지 확인 후 헤더 삭제
      if (api && api.defaults && api.defaults.headers && api.defaults.headers.common) {
        delete api.defaults.headers.common['Authorization'];
      }
    },

    setToken(token, expiresIn = null) {
      this.token = token;
      localStorage.setItem('token', token);
      api.defaults.headers.common['Authorization'] = `Bearer ${token}`;

      if (expiresIn) {
        this.tokenExpiresAt = new Date(Date.now() + expiresIn * 1000);
        localStorage.setItem('tokenExpiresAt', this.tokenExpiresAt.toISOString());
      }
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

        // 토큰 만료 확인
        if (this.tokenExpiresAt && Date.now() >= this.tokenExpiresAt.getTime()) {
          console.log('Token expired, logging out...');
          this.logout();
          return;
        }

        try {
          await this.fetchUser();
          this.startTokenManagement();
        } catch (error) {
          // 토큰이 유효하지 않으면 로그아웃
          console.log('Token validation failed, logging out...');
          this.logout();
        }
      }
    },

    startTokenManagement() {
      this.clearTimer();

      if (!this.tokenExpiresAt || !this.isAdmin) return;

      const timeUntilExpiry = this.tokenExpiresAt.getTime() - Date.now();
      const warningTime = 1 * 60 * 1000; // 1분

      // 만료 1분 전에 팝업 표시
      if (timeUntilExpiry > warningTime) {
        this.warningTimer = setTimeout(() => {
          this.showExpirationPopup();
        }, timeUntilExpiry - warningTime);
      } else if (timeUntilExpiry > 0) {
        // 이미 1분 미만 남았으면 즉시 팝업 표시
        this.showExpirationPopup();
      }
    },

    clearTimer() {
      if (this.warningTimer) {
        clearTimeout(this.warningTimer);
        this.warningTimer = null;
      }
    },

    showExpirationPopup() {
      if (this.isAdmin && this.tokenExpiresAt) {
        const timeLeft = this.tokenExpiresAt.getTime() - Date.now();
        if (timeLeft > 0) {
          const message = '세션이 1분 후에 만료됩니다.\n세션을 연장하시겠습니까?';

          if (confirm(message)) {
            this.refreshToken();
          }
        }
      }
    },
  },
});
