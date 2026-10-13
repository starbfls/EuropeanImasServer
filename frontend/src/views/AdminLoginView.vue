<template>
  <div class="min-h-screen bg-[#07091a] flex items-center justify-center px-4 py-20">
    <div class="w-full max-w-sm">
      <div class="text-center mb-8">
        <img src="/logo.png" alt="Logo" class="h-14 w-14 object-contain mx-auto opacity-90" />
        <p class="text-emerald-400/70 text-xs tracking-[0.3em] uppercase mt-4">Admin</p>
        <h1 class="text-2xl font-extrabold text-white mt-1">管理后台登录</h1>
      </div>

      <form @submit.prevent="handleLogin" class="bg-white/5 border border-white/10 rounded-2xl p-6 space-y-4">
        <div>
          <label class="block text-xs font-bold text-white/50 mb-1.5">用户名</label>
          <input
            v-model="username"
            type="text"
            autocomplete="username"
            class="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-2.5 text-sm text-white placeholder-white/25 focus:outline-none focus:border-emerald-400 transition-colors"
            placeholder="admin"
          />
        </div>

        <div>
          <label class="block text-xs font-bold text-white/50 mb-1.5">密码</label>
          <input
            v-model="password"
            type="password"
            autocomplete="current-password"
            class="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-2.5 text-sm text-white placeholder-white/25 focus:outline-none focus:border-emerald-400 transition-colors"
            placeholder="••••••••"
          />
        </div>

        <p v-if="error" class="text-xs font-bold text-red-400 bg-red-500/10 border border-red-500/20 rounded-lg px-3 py-2">
          {{ error }}
        </p>

        <button
          type="submit"
          :disabled="loading || !username || !password"
          class="w-full bg-emerald-500 hover:bg-emerald-600 text-white font-extrabold rounded-xl py-2.5 text-sm transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
        >
          {{ loading ? '登录中…' : '登录' }}
        </button>
      </form>

      <p class="text-center text-[11px] text-white/25 mt-6">
        账号由服务器 <code class="text-white/40">backend/.env</code> 配置，忘记密码请重新运行 create_admin.py
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { login } from '../api/admin'

const route = useRoute()
const router = useRouter()

const username = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

async function handleLogin() {
  loading.value = true
  error.value = ''
  try {
    await login(username.value, password.value)
    router.replace(route.query.redirect || '/admin')
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}
</script>
