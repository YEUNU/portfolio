<template>
  <div class="login-view">
    <div class="login-form-container">
      <h1 class="form-title">Admin Login</h1>
      <p class="form-subtitle">관리자 계정으로 로그인해주세요.</p>
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="username" class="form-label">Username</label>
          <input
            id="username"
            type="text"
            v-model="username"
            class="form-input"
            required
            placeholder="아이디를 입력하세요"
          />
        </div>
        <div class="form-group">
          <label for="password" class="form-label">Password</label>
          <input
            id="password"
            type="password"
            v-model="password"
            class="form-input"
            required
            placeholder="비밀번호를 입력하세요"
          />
        </div>
        <p v-if="error" class="error-message">{{ error }}</p>
        <button type="submit" class="btn-submit" :disabled="loading">
          {{ loading ? '로그인 중...' : '로그인' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/store/auth';

const username = ref('admin');
const password = ref('password');
const error = ref(null);
const loading = ref(false);

const router = useRouter();
const authStore = useAuthStore();

const handleLogin = async () => {
  loading.value = true;
  error.value = null;
  try {
    // 이제 login 액션은 성공 시 아무것도 반환하지 않고, 실패 시 에러를 throw합니다.
    await authStore.login({
      username: username.value,
      password: password.value,
    });
    
    // 에러가 발생하지 않았다면 로그인 성공으로 간주하고 메인 페이지로 이동합니다.
    router.push({ name: 'Board' });

  } catch (err) {
    // ✅ 수정된 부분: authStore에서 던진 에러 객체의 상세 메시지를 표시합니다.
    error.value = err.message || '알 수 없는 오류가 발생했습니다.';
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.login-view {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
}

.login-form-container {
  width: 100%;
  max-width: 400px;
  padding: 40px;
  background-color: #1e1e1e;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.form-title {
  font-size: 2rem;
  font-weight: bold;
  text-align: center;
  margin-bottom: 10px;
  color: #fff;
}

.form-subtitle {
  text-align: center;
  color: #a0a0a0;
  margin-bottom: 30px;
}

.form-group {
  margin-bottom: 20px;
}

.form-label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #c0c0c0;
}

.form-input {
  width: 100%;
  padding: 12px 16px;
  background-color: #2a2a2a;
  border: 1px solid #444;
  border-radius: 8px;
  color: #e0e0e0;
  font-size: 1rem;
  transition: border-color 0.2s ease;
}

.form-input:focus {
  outline: none;
  border-color: #3d8bfd;
}

.error-message {
  color: #e57373;
  text-align: center;
  margin-bottom: 20px;
}

.btn-submit {
  width: 100%;
  padding: 14px;
  border: none;
  border-radius: 8px;
  background-color: #3d8bfd;
  color: #fff;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.btn-submit:hover {
  background-color: #2a79e8;
}

.btn-submit:disabled {
  background-color: #555;
  cursor: not-allowed;
}
</style>

