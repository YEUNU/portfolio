&lt;template> &lt;div class="post-card" @click="$emit('click')"> &lt;div class="post-thumbnail"
:style="thumbnailStyle" >&lt;/div> &lt;div class="post-info"> &lt;h2 class="post-title">{{
  post.title
}}&lt;/h2> &lt;p class="post-tags">{{ post.tags }}&lt;/p> &lt;div v-if="showAdmin"
class="admin-actions"> &lt;BaseButton variant="primary" @click.stop="$emit('edit')" > 수정
&lt;/BaseButton> &lt;BaseButton variant="danger" @click.stop="$emit('delete')" > 삭제
&lt;/BaseButton> &lt;/div> &lt;/div> &lt;/div> &lt;/template> &lt;script setup> import { computed }
from 'vue'; import api from '@/services/api'; import BaseButton from
'@/components/common/BaseButton.vue'; const props = defineProps({ post: { type: Object, required:
true }, showAdmin: { type: Boolean, default: false } }); const thumbnailStyle = computed(() => {
const firstImage = extractFirstImage(props.post.content); if (firstImage) { const fullUrl =
firstImage.startsWith('/') ? `${api.defaults.baseURL}${firstImage}` : firstImage; return {
backgroundImage: `url(${fullUrl})` }; } return {}; }); function extractFirstImage(content) { if
(!content) return null; const regex = /!\[.*?\]\((.*?)\)/; const match = content.match(regex);
return match ? match[1] : null; } defineEmits(['click', 'edit', 'delete']); &lt;/script> &lt;style
scoped> .post-card { background-color: var(--color-surface); border-radius: var(--border-radius);
overflow: hidden; transition: transform var(--transition-speed) ease-in-out, box-shadow
var(--transition-speed) ease-in-out; cursor: pointer; } .post-card:hover { transform:
translateY(-5px); box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2); } .post-thumbnail { width: 100%;
height: 200px; background-color: var(--color-surface-light); background-size: cover;
background-position: center; background-repeat: no-repeat; } .post-info { padding:
var(--spacing-md); } .post-title { font-size: 1.2rem; font-weight: 600; margin: 0 0
var(--spacing-sm) 0; color: var(--color-text); } .post-tags { font-size: 0.9rem; color:
var(--color-text-dark); margin-bottom: var(--spacing-sm); } .admin-actions { display: flex; gap:
var(--spacing-sm); margin-top: var(--spacing-sm); } &lt;/style>
