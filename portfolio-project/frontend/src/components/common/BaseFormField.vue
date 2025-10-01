&lt;template>
  &lt;div class="form-field">
    &lt;label v-if="label" :for="id" class="form-label">{{ label }}&lt;/label>
    &lt;textarea
      v-if="type === 'textarea'"
      :id="id"
      :value="modelValue"
      @input="$emit('update:modelValue', $event.target.value)"
      v-bind="$attrs"
      class="form-input"
      :rows="rows"
    >&lt;/textarea>
    &lt;input
      v-else
      :id="id"
      :type="type"
      :value="modelValue"
      @input="$emit('update:modelValue', $event.target.value)"
      v-bind="$attrs"
      class="form-input"
    >
  &lt;/div>
&lt;/template>

&lt;script setup>
import { computed } from 'vue';

const props = defineProps({
  label: {
    type: String,
    default: ''
  },
  modelValue: {
    type: [String, Number],
    default: ''
  },
  type: {
    type: String,
    default: 'text'
  },
  rows: {
    type: Number,
    default: 5
  }
});

const id = computed(() => `form-field-${Math.random().toString(36).substr(2, 9)}`);

defineEmits(['update:modelValue']);
&lt;/script>

&lt;style scoped>
.form-field {
  margin-bottom: 1.5rem;
}

.form-label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #e0e0e0;
}

.form-input {
  width: 100%;
  padding: 0.8rem;
  background-color: #2a2a2a;
  border: 1px solid #444;
  border-radius: 8px;
  color: #e0e0e0;
  font-size: 1rem;
  transition: border-color 0.2s;
}

.form-input:focus {
  outline: none;
  border-color: #3d8bfd;
}

textarea.form-input {
  resize: vertical;
  min-height: 100px;
}
&lt;/style>