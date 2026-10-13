<template>
  <div class="min-h-screen bg-[#f9f8f6]">
    <!-- Header -->
    <div class="bg-[#07091a] border-b border-white/5 py-12 px-4">
      <div class="max-w-4xl mx-auto">
        <p class="text-white/30 text-xs tracking-[0.3em] uppercase mb-2">Rules & Links</p>
        <h1 class="text-3xl font-extrabold text-white">规章 & 链接</h1>
        <p class="text-white/40 text-sm mt-2">加入前请阅读社群规章，共同维护良好的社群环境。</p>
      </div>
    </div>

    <div class="max-w-4xl mx-auto px-4 py-12">
      <!-- Join CTAs -->
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-14">
        <!-- Discord -->
        <RouterLink
          to="/discord"
          class="group relative overflow-hidden flex items-center gap-5 bg-[#5865F2] hover:bg-[#4752e0] text-white rounded-2xl p-6 shadow-lg transition-all duration-200 hover:-translate-y-1 hover:shadow-xl"
        >
          <img
            src="/assets/brand/lilja-sd.webp"
            alt="葛城莉莉娅 Q 版立绘"
            class="h-28 w-auto shrink-0 -my-3 drop-shadow-lg transition-transform duration-300 group-hover:-translate-y-1"
          />
          <div>
            <p class="text-xs uppercase font-extrabold text-indigo-200 tracking-wider mb-1">Chat with us</p>
            <p class="text-xl font-extrabold leading-tight">Discord 服务器</p>
            <p class="text-xs text-indigo-200 mt-1">正在创建中，点击查看进度</p>
          </div>
        </RouterLink>

        <!-- QQ — opens QR modal -->
        <button
          @click="showQR = true"
          class="group flex items-center gap-5 bg-sky-500 hover:bg-sky-600 text-white rounded-2xl p-6 shadow-lg transition-all duration-200 hover:-translate-y-1 hover:shadow-xl w-full text-left"
        >
          <img src="/assets/brand/group-avatar.png" alt="群头像"
            class="h-16 w-16 rounded-full shrink-0 ring-2 ring-white/40 transition-transform duration-300 group-hover:scale-105" />
          <div>
            <p class="text-xs uppercase font-extrabold text-sky-200 tracking-wider mb-1">Join us on</p>
            <p class="text-xl font-extrabold leading-tight">QQ 制作人群</p>
            <p class="text-xs text-sky-200 mt-1">点击查看二维码，扫码加入</p>
          </div>
        </button>
      </div>

      <!-- Rules sections -->
      <div class="space-y-5">
        <div
          v-for="(sec, i) in rules"
          :key="i"
          class="bg-white rounded-2xl shadow-sm p-6 border-l-4"
          :class="sec.border"
        >
          <h2 class="text-base font-extrabold text-gray-900 mb-5 flex items-center gap-2.5">
            <span class="text-xl">{{ sec.icon }}</span>
            {{ sec.title }}
          </h2>
          <ol class="space-y-3">
            <li
              v-for="(rule, j) in sec.items"
              :key="j"
              class="flex items-start gap-3 text-gray-600 text-sm"
            >
              <span class="text-xs font-extrabold text-gray-300 w-5 shrink-0 mt-0.5">{{ j + 1 }}.</span>
              <span class="leading-relaxed">{{ rule }}</span>
            </li>
          </ol>
        </div>
      </div>

      <p class="mt-10 text-center text-xs text-gray-400">
        加入社群即表示你同意遵守以上规章。规章可能随时更新，请定期查看。
      </p>
    </div>

    <!-- QQ QR Code Modal -->
    <Transition name="fade">
      <div
        v-if="showQR"
        class="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm px-4"
        @click.self="showQR = false"
      >
        <div class="bg-white rounded-3xl shadow-2xl p-8 max-w-xs w-full flex flex-col items-center text-center">
          <!-- Close button -->
          <button
            @click="showQR = false"
            class="self-end -mt-2 -mr-2 mb-4 w-8 h-8 rounded-full bg-gray-100 hover:bg-gray-200 text-gray-500 flex items-center justify-center transition-colors text-lg font-bold leading-none"
            aria-label="关闭"
          >
            ×
          </button>

          <p class="text-xs uppercase tracking-[0.25em] text-sky-400 font-extrabold mb-1">QQ 制作人群</p>
          <p class="text-base font-extrabold text-gray-900 mb-5">欧洲偶像大师制作人群</p>

          <img
            src="/groupqrcode.png"
            alt="QQ群二维码"
            class="w-52 h-52 object-contain bg-white rounded-2xl border border-gray-100 p-2 shadow-sm"
          />

          <p class="mt-5 text-sm text-gray-500 leading-relaxed">
            打开 QQ，扫描上方二维码<br />即可申请加入制作人群
          </p>
          <button
            @click="showQR = false"
            class="mt-5 px-6 py-2 bg-sky-500 hover:bg-sky-600 text-white rounded-full text-sm font-bold transition-colors"
          >
            关闭
          </button>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const showQR = ref(false)

const rules = [
  {
    icon: '🤝',
    title: '基本行为准则',
    border: 'border-sky-400',
    items: [
      '尊重并友好对待所有成员，无论其国籍、背景或所推的偶像大师分支。',
      '严禁任何形式的骚扰、霸凌或仇恨言论。社群面向所有人开放。',
      '欢迎理性讨论，但禁止人身攻击。请对事不对人。',
      '尊重他人隐私，未经同意不得泄露或传播其个人信息。',
    ],
  },
  {
    icon: '🎵',
    title: '内容规范',
    border: 'border-purple-400',
    items: [
      '发布内容应与偶像大师及粉丝社群活动相关。',
      '严禁传播盗版资源，包括非法直播流、破解文件及未授权的游戏内容。',
      '转载他人同人作品时必须注明原作者。严禁冒充他人作品。',
      '全年龄向社群，严禁发布任何NSFW内容。',
    ],
  },
  {
    icon: '📅',
    title: '活动与聚会',
    border: 'border-green-400',
    items: [
      '参加线下聚会请提前在 Discord 频道报名，方便主办方安排。',
      '如有特殊情况无法出席，请尽早在群内说明，不要无故爽约。',
      '参加线下活动时，请注意公共场合秩序，维护良好形象。',
      '拍摄并发布其他成员的照片前，请事先征得本人同意。',
    ],
  },
  {
    icon: '⚠️',
    title: '违规处理',
    border: 'border-amber-400',
    items: [
      '管理员有权根据违规情节轻重，对成员采取警告、禁言或封禁等措施。',
      '初次轻微违规通常给予正式警告。',
      '多次违规或严重不当行为可能导致直接永久封禁。',
      '如遇违规行为，请向管理员举报，切勿与当事人正面冲突。',
    ],
  },
]
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
