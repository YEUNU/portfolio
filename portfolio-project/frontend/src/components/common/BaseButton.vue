<template>
  <button
    :class="['base-button', variant, { disabled: disabled }]"
    :disabled="disabled"
    v-bind="$attrs"
  >
    <slot></slot>
  </button>
</template>

<script setup>
defineProps({
  variant: {
    type: String,
    default: 'primary',
    validator: (value) => ['primary', 'secondary', 'danger'].includes(value),
  },
  disabled: {
    type: Boolean,
    default: false,
  },
});
</script>

<style scoped>
.base-button {
  padding: 0.8rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s, opacity 0.2s;
}

.primary {
  background-color: #3d8bfd;
  color: white;
}

.primary:hover:not(.disabled) {
  background-color: #2a79e8;
}

.secondary {
  background-color: #2a2a2a;
  color: #e0e0e0;
}

.secondary:hover:not(.disabled) {
  background-color: #333;
}

.danger {
  background-color: #e53935;
  color: white;
}

.danger:hover:not(.disabled) {
  background-color: #d32f2f;
}

.disabled {
  opacity: 0.7;
  cursor: not-allowed;
}
</style>
