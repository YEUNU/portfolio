<template>
  <button
    :class="buttonClasses"
    :disabled="disabled"
    v-bind="$attrs"
  >
    <slot></slot>
  </button>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  variant: {
    type: String,
    default: 'primary',
    validator: (value) => ['primary', 'secondary', 'danger', 'success', 'outline'].includes(value),
  },
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['sm', 'md', 'lg'].includes(value),
  },
  disabled: {
    type: Boolean,
    default: false,
  },
});

const buttonClasses = computed(() => {
  const baseClasses = 'inline-flex items-center justify-center font-medium transition-all duration-200 focus:outline-none';
  
  const sizeClasses = {
    sm: 'px-4 py-2 text-sm rounded-md3-sm h-10',
    md: 'px-6 py-2.5 text-base rounded-md3-md h-12',
    lg: 'px-8 py-3 text-lg rounded-md3-lg h-14',
  };
  
  const variantClasses = {
    primary: 'bg-primary hover:bg-primary-dark dark:bg-primary-dark dark:hover:bg-primary text-primary-on shadow-md3-2 hover:shadow-md3-3 focus:shadow-md3-3',
    secondary: 'bg-primary-100 hover:bg-primary-200 dark:bg-primary-800 dark:hover:bg-primary-700 text-primary-900 dark:text-primary-100 shadow-md3-1 hover:shadow-md3-2',
    danger: 'bg-error hover:bg-error-dark dark:bg-error-dark dark:hover:bg-error text-error-on shadow-md3-2 hover:shadow-md3-3',
    success: 'bg-primary-200 hover:bg-primary-300 dark:bg-primary-700 dark:hover:bg-primary-600 text-primary-900 dark:text-primary-100 shadow-md3-2 hover:shadow-md3-3',
    outline: 'bg-transparent border border-outline dark:border-outline-dark hover:bg-surface-variant/50 dark:hover:bg-surface-dark-variant/50 text-primary dark:text-primary-dark',
  };
  
  const disabledClasses = props.disabled ? 'opacity-38 cursor-not-allowed' : 'cursor-pointer hover:scale-[1.02] active:scale-[0.98]';
  
  return [
    baseClasses,
    sizeClasses[props.size],
    variantClasses[props.variant],
    disabledClasses,
  ].join(' ');
});
</script>
