<template>
  <div class="mb-4">
    <label 
      v-if="label" 
      :for="id" 
      class="block text-sm font-medium text-surface-on dark:text-surface-dark-on mb-2"
    >
      {{ label }}
    </label>
    <textarea
      v-if="type === 'textarea'"
      :id="id"
      :value="modelValue"
      @input="$emit('update:modelValue', $event.target.value)"
      v-bind="$attrs"
      :rows="rows"
      class="w-full px-4 py-3 bg-surface dark:bg-surface-dark border border-outline dark:border-outline-dark rounded-md3-md text-surface-on dark:text-surface-dark-on placeholder-surface-on-variant dark:placeholder-surface-dark-on focus:outline-none focus:border-primary dark:focus:border-primary-dark focus:shadow-md3-1 transition-all duration-200 resize-vertical min-h-[100px]"
    ></textarea>
    <input
      v-else
      :id="id"
      :type="type"
      :value="modelValue"
      @input="$emit('update:modelValue', $event.target.value)"
      v-bind="$attrs"
      class="w-full px-4 py-3 bg-surface dark:bg-surface-dark border border-outline dark:border-outline-dark rounded-md3-md text-surface-on dark:text-surface-dark-on placeholder-surface-on-variant dark:placeholder-surface-dark-on focus:outline-none focus:border-primary dark:focus:border-primary-dark focus:shadow-md3-1 transition-all duration-200"
    />
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  label: {
    type: String,
    default: '',
  },
  modelValue: {
    type: [String, Number],
    default: '',
  },
  type: {
    type: String,
    default: 'text',
  },
  rows: {
    type: Number,
    default: 5,
  },
});

const id = computed(() => `form-field-${Math.random().toString(36).substr(2, 9)}`);

defineEmits(['update:modelValue']);
</script>
