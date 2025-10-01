<template>
  <div class="login-view">
    <div class="login-form-container">
      <h1 class="form-title">Admin Login</h1>
      <p class="form-subtitle">관리자 계정으로 로그인해주세요.</p>
      <form @submit.prevent="handleLogin" class="login-form">
        <BaseFormField
          v-model="username"
          label="Username"
          type="text"
          placeholder="아이디를 입력하세요"
          required
        />
        <BaseFormField
          v-model="password"
          label="Password"
          type="password"
          placeholder="비밀번호를 입력하세요"
          required
        />
        <p v-if="error" class="error-message">{{ error }}</p>
        <BaseButton
          type="submit"
          :disabled="loading"
          class="login-button"
        >
          {{ loading ? '로그인 중...' : '로그인' }}
        </BaseButton>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/store/auth';
import BaseButton from '@/components/common/BaseButton.vue';
import BaseFormField from '@/components/common/BaseFormField.vue';

const username = ref('');
const password = ref('');
const error = ref(null);
const loading = ref(false);

const router = useRouter();
const authStore = useAuthStore();

const handleLogin = async () => {
  loading.value = true;
  error.value = null;
  
  try {
    await authStore.login({
      username: username.value,
      password: password.value,
    });
    router.push({ name: 'Board' });
  } catch (err) {
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
  padding: var(--spacing-lg);
}

.login-form-container {
  width: 100%;
  max-width: 400px;
  padding: var(--spacing-xl);
  background-color: var(--color-surface);
  border-radius: var(--border-radius);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.form-title {
  font-size: 2rem;
  font-weight: bold;
  text-align: center;
  margin-bottom: var(--spacing-xs);
  color: var(--color-text);
}

.form-subtitle {
  text-align: center;
  color: var(--color-text-light);
  margin-bottom: var(--spacing-lg);
}

.error-message {
  color: var(--color-error);
  text-align: center;
  margin: var(--spacing-md) 0;
}

.login-button {
  width: 100%;
  padding: var(--spacing-sm) 0;
  font-size: 1.1rem;
  font-weight: 600;
}
</style>