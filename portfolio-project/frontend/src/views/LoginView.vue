&lt;template>
  &lt;div class="login-view">
    &lt;div class="login-form-container">
      &lt;h1 class="form-title">Admin Login&lt;/h1>
      &lt;p class="form-subtitle">관리자 계정으로 로그인해주세요.&lt;/p>
      &lt;form @submit.prevent="handleLogin" class="login-form">
        &lt;BaseFormField
          v-model="username"
          label="Username"
          type="text"
          placeholder="아이디를 입력하세요"
          required
        />
        &lt;BaseFormField
          v-model="password"
          label="Password"
          type="password"
          placeholder="비밀번호를 입력하세요"
          required
        />
        &lt;p v-if="error" class="error-message">{{ error }}&lt;/p>
        &lt;BaseButton
          type="submit"
          :disabled="loading"
          class="login-button"
        >
          {{ loading ? '로그인 중...' : '로그인' }}
        &lt;/BaseButton>
      &lt;/form>
    &lt;/div>
  &lt;/div>
&lt;/template>

&lt;script setup>
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
&lt;/script>

&lt;style scoped>
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
&lt;/style>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/store/auth';

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

