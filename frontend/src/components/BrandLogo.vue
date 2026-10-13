<template>
  <div
    class="brand-logo select-none"
    :class="[`brand-logo--${size}`, `brand-logo--${align}`]"
    role="img"
    aria-label="468 Production 欧洲活動部 — IM@S Europe Branch"
  >
    <!-- 主行：468 Production 欧洲活動部 -->
    <div class="row" aria-hidden="true">
      <!-- 468 读作ヨーロッパ，假名固定压在各自数字正上方 -->
      <span class="digits">
        <span v-for="d in DIGITS" :key="d.n" class="digit">
          <span class="digit__kana">{{ d.kana }}</span>
          <span class="digit__num">{{ d.n }}</span>
        </span>
      </span>

      <span class="word-pro">Production</span>

      <span class="word-cn">
        <span v-for="c in CN" :key="c.t" :style="{ color: c.c }">{{ c.t }}</span>
      </span>
    </div>

    <!-- 副行：细线夹住的英文 -->
    <div class="tagline-row" aria-hidden="true">
      <span class="rule" />
      <span class="tagline">IM<span class="at">@</span>S EUROPE BRANCH</span>
      <span class="rule" />
    </div>
  </div>
</template>

<script setup>
// 468 = ヨーロッパ 的语呂合わせ：4→ヨー、6→ロッ、8→パ
const DIGITS = [
  { n: '4', kana: 'ヨー' },
  { n: '6', kana: 'ロッ' },
  { n: '8', kana: 'パ' },
]

// 逐字配色取自现行 logo
const CN = [
  { t: '欧', c: '#3d8ee0' },
  { t: '洲', c: '#f2c94c' },
  { t: '活', c: '#3fc9a0' },
  { t: '動', c: '#7fb8ee' },
  { t: '部', c: '#f2994a' },
]

defineProps({
  // hero 用 lg，导航栏和页脚用 sm
  size: { type: String, default: 'lg' },
  // 页脚里要左对齐，其余居中
  align: { type: String, default: 'center' },
})
</script>

<style scoped>
.brand-logo {
  font-family: 'Space Grotesk', 'Nunito', sans-serif;
  font-weight: 700;
  line-height: 1;
}

.brand-logo--start .row,
.brand-logo--start .tagline-row { justify-content: flex-start; }

/* 尺寸只调基准字号，内部全部用 em 跟随 */
.brand-logo--lg { font-size: clamp(1.6rem, 5.8vw, 4.25rem); }
.brand-logo--sm { font-size: 1rem; }

.row {
  display: flex;
  align-items: baseline;
  justify-content: center;
  gap: 0.3em;
  white-space: nowrap;
}

/* ── 468 + 振假名 ───────────────────────────────────────────────────────── */
.digits { display: flex; align-items: baseline; }

.digit {
  position: relative;
  display: inline-block;
  /* 假名绝对定位在数字上方，所以数字宽度说了算，不会被假名撑开 */
}
.digit__num {
  display: block;
  font-size: 1em;
  letter-spacing: -0.015em;
  background: linear-gradient(180deg, #8fcdf8 0%, #3a7fd0 52%, #1e468f 100%);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  -webkit-text-fill-color: transparent;
}
.digit__kana {
  position: absolute;
  left: 50%;
  bottom: 100%;
  transform: translateX(-50%);
  margin-bottom: 0.06em;
  font-family: 'Noto Sans JP', 'Nunito', system-ui, sans-serif;
  font-size: 0.23em;
  font-weight: 700;
  letter-spacing: 0.02em;
  line-height: 1;
  white-space: nowrap;
  color: #8fb6e8;
  opacity: 0.8;
}
/* 小尺寸下假名挤成一团，不如不要 */
.brand-logo--sm .digit__kana { display: none; }

/* ── Production ────────────────────────────────────────────────────────── */
.word-pro {
  font-size: 0.62em;
  font-style: italic;
  letter-spacing: -0.01em;
  background: linear-gradient(180deg, #ffa8ca 0%, #f2609b 58%, #d63a7c 100%);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  -webkit-text-fill-color: transparent;
}

/* ── 欧洲活動部 ─────────────────────────────────────────────────────────── */
.word-cn {
  font-family: 'Noto Sans SC', 'Noto Sans JP', 'Nunito', system-ui, sans-serif;
  font-size: 0.82em;
  font-weight: 800;
  letter-spacing: 0.03em;
}

/* ── 副行 ──────────────────────────────────────────────────────────────── */
.tagline-row {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.7em;
  margin-top: 0.34em;
}
.tagline {
  font-size: 0.16em;
  font-weight: 700;
  letter-spacing: 0.4em;
  text-indent: 0.4em;
  color: rgba(255, 255, 255, 0.5);
  white-space: nowrap;
}
.at { color: var(--eu-gold); }
.rule {
  height: 1px;
  width: 1.4em;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
}
.brand-logo--sm .tagline { font-size: 0.42em; letter-spacing: 0.2em; text-indent: 0.2em; }
.brand-logo--sm .tagline-row { margin-top: 0.2em; gap: 0.5em; }
.brand-logo--sm .rule { width: 1.8em; }

/* 渐变裁切失效时退回纯色，免得整段变透明 */
@supports not ((-webkit-background-clip: text) or (background-clip: text)) {
  .digit__num { color: #4f93d8; -webkit-text-fill-color: #4f93d8; }
  .word-pro { color: #f2609b; -webkit-text-fill-color: #f2609b; }
}
</style>
