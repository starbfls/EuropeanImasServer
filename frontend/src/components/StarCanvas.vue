<template>
  <canvas ref="canvas" class="absolute inset-0 w-full h-full" />
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const canvas = ref(null)
let animId = null
let stars = []
let shooters = []
let lastShooterTime = 0

function mkStars(w, h, count) {
  return Array.from({ length: count }, () => ({
    x: Math.random() * w,
    y: Math.random() * h,
    r: Math.random() * 1.4 + 0.2,
    op: Math.random() * 0.7 + 0.3,
    td: Math.random() > 0.5 ? 1 : -1,
    ts: Math.random() * 0.008 + 0.003,
    drift: Math.random() * 0.04 + 0.01,
  }))
}

function addShooter(w, h) {
  const angle = (Math.random() * 30 + 10) * (Math.PI / 180)
  shooters.push({
    x: Math.random() * w * 0.8,
    y: Math.random() * h * 0.4,
    vx: Math.cos(angle) * (Math.random() * 6 + 5),
    vy: Math.sin(angle) * (Math.random() * 3 + 2),
    len: Math.random() * 90 + 50,
    life: 1,
    decay: Math.random() * 0.02 + 0.015,
  })
}

function draw(ctx, w, h, now) {
  ctx.clearRect(0, 0, w, h)

  const grad = ctx.createLinearGradient(0, 0, w * 0.3, h)
  grad.addColorStop(0, '#07091a')
  grad.addColorStop(0.5, '#0b1020')
  grad.addColorStop(1, '#0e1428')
  ctx.fillStyle = grad
  ctx.fillRect(0, 0, w, h)

  for (const s of stars) {
    s.op += s.ts * s.td
    if (s.op > 1) { s.op = 1; s.td = -1 }
    if (s.op < 0.15) { s.op = 0.15; s.td = 1 }
    s.y -= s.drift
    if (s.y < -2) { s.y = h + 2; s.x = Math.random() * w }

    ctx.beginPath()
    ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2)
    ctx.fillStyle = s.r > 1 ? `rgba(220,235,255,${s.op})` : `rgba(255,255,255,${s.op})`
    ctx.fill()
  }

  if (now - lastShooterTime > 4500 + Math.random() * 4000) {
    addShooter(w, h)
    lastShooterTime = now
  }
  for (let i = shooters.length - 1; i >= 0; i--) {
    const s = shooters[i]
    s.life -= s.decay
    if (s.life <= 0) { shooters.splice(i, 1); continue }
    const tailX = s.x - s.vx * (s.len / 10)
    const tailY = s.y - s.vy * (s.len / 10)
    const g = ctx.createLinearGradient(tailX, tailY, s.x, s.y)
    g.addColorStop(0, 'rgba(255,255,255,0)')
    g.addColorStop(1, `rgba(255,255,255,${s.life * 0.9})`)
    ctx.beginPath()
    ctx.moveTo(tailX, tailY)
    ctx.lineTo(s.x, s.y)
    ctx.strokeStyle = g
    ctx.lineWidth = 1.5
    ctx.stroke()
    s.x += s.vx
    s.y += s.vy
  }
}

onMounted(() => {
  const el = canvas.value
  const parent = el.parentElement
  const ctx = el.getContext('2d')
  let cssW = 0
  let cssH = 0

  const resize = () => {
    const dpr = Math.min(window.devicePixelRatio || 1, 2)
    cssW = parent.offsetWidth
    cssH = parent.offsetHeight
    el.width = Math.round(cssW * dpr)
    el.height = Math.round(cssH * dpr)
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0)
    stars = mkStars(cssW, cssH, cssW < 640 ? 110 : 180)
  }
  resize()

  const loop = () => {
    draw(ctx, cssW, cssH, performance.now())
    animId = requestAnimationFrame(loop)
  }
  loop()

  const ro = new ResizeObserver(resize)
  ro.observe(parent)
  onUnmounted(() => {
    cancelAnimationFrame(animId)
    ro.disconnect()
  })
})
</script>
