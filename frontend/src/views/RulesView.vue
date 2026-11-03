<template>
  <div class="handbook">
    <section class="handbook-hero">
      <div class="hero-grid" aria-hidden="true"></div>
      <div class="page-width hero-content">
        <div class="hero-copy">
          <p class="eyebrow"><span></span> 468 PRODUCTION · COMMUNITY HANDBOOK</p>
          <h1>欢迎来到<br /><span>468 事务所。</span></h1>
          <p class="hero-description">欧洲偶像大师同好会 · 新人入群手册</p>
          <div class="hero-actions">
            <a href="#guidelines" class="button button-gold">阅读社群规章 <span aria-hidden="true">↓</span></a>
            <a href="#join" class="hero-join">加入 QQ 制作人群 <span aria-hidden="true">↗</span></a>
          </div>
        </div>
        <div class="office-note">
          <p class="eyebrow">A PLACE FOR EVERY PRODUCER</p>
          <p class="office-motto">不论担当是谁，<br />都在这里相聚。</p>
          <p class="office-description">从欧洲时区出发，和世界各地的伙伴一起聊偶像、聊现场，为喜欢的偶像应援。</p>
          <div class="office-stamp" aria-hidden="true"><span>468</span><small>PRODUCTION</small></div>
        </div>
      </div>
    </section>

    <div class="page-width handbook-layout">
      <aside class="contents" aria-label="手册目录">
        <div class="contents-inner">
          <p class="eyebrow">在这里，先认识彼此</p>
          <nav aria-label="本页导航">
            <a href="#community"><span>00</span> 我们的同好会</a>
            <a v-for="section in sections" :key="section.id" :href="'#' + section.id">
              <span>{{ section.number }}</span> {{ section.shortTitle }}
            </a>
            <a href="#join"><span>04</span> 加入事务所</a>
          </nav>
          <p class="sidebar-note">欢迎畅所欲言，<br />也请照顾彼此的感受。</p>
        </div>
      </aside>

      <div class="handbook-body">
        <section id="community" class="community-section anchor-section" aria-labelledby="community-title">
          <p class="eyebrow section-label">00 / ABOUT US</p>
          <h2 id="community-title">欧洲时区，同一份热爱。</h2>
          <p class="body-copy">这里是偶像大师欧洲同好会——468 事务所。身处欧洲多国、东亚、南美和北美，拥有海外留学经历的制作人在这里相聚。</p>
          <p class="body-copy">我们主要聊偶像大师系列，对所有企划及声优相关内容开放。无论你喜欢哪一个企划、担当哪一位偶像，都欢迎加入讨论。</p>
          <ul class="brand-list" aria-label="欢迎所有偶像大师企划的制作人">
            <li v-for="brand in brands" :key="brand.name" :style="{ '--brand-color': brand.color }">
              <span class="brand-code">{{ brand.code }}</span><span>{{ brand.name }}</span>
            </li>
          </ul>
        </section>

        <section id="guidelines" class="guidelines-intro anchor-section" aria-labelledby="guidelines-title">
          <p class="eyebrow section-label">BEFORE YOU JOIN</p>
          <h2 id="guidelines-title">让交流舒服一点。</h2>
          <p class="body-copy">入群前，请读完下面的约定。希望大家和谐相处，一起为担当偶像应援。</p>
          <div class="quick-rules" aria-label="基本注意事项">
            <span>不人身攻击、不骚扰</span><span>不引战、不拉踩</span><span>不聊政治、不发 R18</span><span>少发鬼图、不刷屏</span>
          </div>
        </section>

        <section v-for="section in sections" :id="section.id" :key="section.id"
          class="rule-section anchor-section" :aria-labelledby="section.id + '-title'">
          <div class="rule-heading">
            <span class="section-number" aria-hidden="true">{{ section.number }}</span>
            <div>
              <p class="eyebrow section-label">{{ section.kicker }}</p>
              <h2 :id="section.id + '-title'">{{ section.title }}</h2>
            </div>
          </div>
          <p class="section-intro">{{ section.intro }}</p>
          <ul class="rule-list">
            <li v-for="rule in section.rules" :key="rule.title">
              <span class="rule-dot" aria-hidden="true"></span>
              <div><h3>{{ rule.title }}</h3><p>{{ rule.description }}</p></div>
            </li>
          </ul>
        </section>

        <section class="moderation" aria-labelledby="moderation-title">
          <div class="moderation-symbol" aria-hidden="true">!</div>
          <div>
            <p class="eyebrow">MODERATION</p>
            <h2 id="moderation-title">规章需要大家一起遵守。</h2>
            <p>违反以上约定，管理员将视情节轻重予以警告、禁言或移出群聊。</p>
            <div class="moderation-actions"><span>警告</span><i aria-hidden="true">/</i><span>禁言</span><i aria-hidden="true">/</i><span>移出群聊</span></div>
          </div>
        </section>

        <section id="join" class="join-section anchor-section" aria-labelledby="join-title">
          <div class="join-copy">
            <p class="eyebrow section-label">04 / JOIN THE COMMUNITY</p>
            <h2 id="join-title">下一位 Producer，<br />欢迎入座。</h2>
            <p class="body-copy">读完手册，就来和大家打个招呼吧。打开 QQ 扫描二维码申请加入，也可以保存图片，在 QQ 内识别。</p>
          </div>
          <div class="qr-card">
            <button type="button" class="qr-trigger" aria-label="放大QQ群二维码" @click="openQR">
              <span class="qr-crop"><img :src="qrImage" alt="QQ群二维码" width="1284" height="2283" /></span>
              <span class="qr-caption">点击放大二维码 <span aria-hidden="true">⤢</span></span>
            </button>
            <a :href="qrImage" target="_blank" rel="noopener" class="original-link">打开原图 <span aria-hidden="true">↗</span></a>
          </div>
        </section>
        <p class="closing-note">欢迎各位 Producer 来到本事务所。一起为担当偶像应援！</p>
      </div>
    </div>

    <dialog ref="qrDialog" class="qr-dialog" aria-labelledby="qr-title" aria-describedby="qr-description"
      @click="onDialogClick" @close="onDialogClose" @keydown.tab="keepDialogFocus">
      <div class="qr-dialog-content">
        <div class="qr-dialog-heading">
          <div><p class="eyebrow section-label">QQ PRODUCER COMMUNITY</p><h2 id="qr-title">扫码加入 468 事务所</h2></div>
          <button type="button" class="dialog-close" aria-label="关闭二维码大图" @click="qrDialog.close()">×</button>
        </div>
        <div class="qr-crop qr-large"><img :src="qrImage" alt="QQ群二维码大图" width="1284" height="2283" /></div>
        <p id="qr-description" class="dialog-description">打开 QQ 扫一扫，或在手机相册中识别二维码。</p>
        <div class="dialog-actions">
          <a :href="qrImage" target="_blank" rel="noopener" class="button button-dark">打开完整原图 ↗</a>
          <a :href="qrImage" download="468事务所-QQ群二维码.jpg" class="download-link">下载二维码</a>
        </div>
      </div>
    </dialog>
  </div>
</template>

<script setup>
import { onBeforeUnmount, ref } from 'vue'

const qrImage = '/assets/community/group-qrcode.jpg'
const qrDialog = ref(null)
let previousOverflow = ''

function openQR() {
  if (qrDialog.value?.open) return
  previousOverflow = document.body.style.overflow
  qrDialog.value.showModal()
  document.body.style.overflow = 'hidden'
}
function onDialogClick(event) {
  if (event.target === qrDialog.value) qrDialog.value.close()
}
function onDialogClose() {
  document.body.style.overflow = previousOverflow
}
function keepDialogFocus(event) {
  const controls = qrDialog.value.querySelectorAll('button, a[href]')
  const first = controls[0]
  const last = controls[controls.length - 1]
  if (event.shiftKey && document.activeElement === first) {
    event.preventDefault()
    last.focus()
  } else if (!event.shiftKey && document.activeElement === last) {
    event.preventDefault()
    first.focus()
  }
}
onBeforeUnmount(() => {
  if (qrDialog.value?.open) {
    qrDialog.value.close()
    document.body.style.overflow = previousOverflow
  }
})

const brands = [
  { code: '765', name: '本家', color: '#ce526c' },
  { code: 'CG', name: '灰姑娘女孩', color: '#407db4' },
  { code: 'ML', name: '百万现场', color: '#b68912' },
  { code: 'SideM', name: 'SideM', color: '#409079' },
  { code: 'SC', name: '闪耀色彩', color: '#6989bc' },
  { code: '学マス', name: '学园偶像大师', color: '#bd7146' },
]

const sections = [
  {
    id: 'respect', number: '01', shortTitle: '尊重彼此',
    kicker: 'RESPECT EVERY PRODUCER', title: '尊重每一份喜欢。',
    intro: '你可以不是某个企划或偶像的担当，但请尊重其他制作人的喜好。',
    rules: [
      { title: '禁止人身攻击与无端骚扰', description: '不引战、不拉踩，不以言语或行为攻击、骚扰其他成员。欢迎交流不同看法，也请保持基本尊重。' },
      { title: '不侮辱偶像、声优与制作人', description: '禁止人格侮辱、恶意调侃愚弄、诋毁诽谤，也不要把圈内梗当作中伤他人的工具。' },
      { title: '对所有企划保持尊重', description: '本家、灰姑娘、百万现场、SideM、闪耀色彩、学园偶像大师的制作人，都是这个小屋的一员。请勿发表贬低偶像或企划的言论。' },
    ],
  },
  {
    id: 'boundaries', number: '02', shortTitle: '玩梗与内容边界',
    kicker: 'KEEP THE CONVERSATION COMFORTABLE', title: '适度玩梗，记得分寸。',
    intro: '偶大圈内梗虽多，也请照顾他人的感受和浏览体验。',
    rules: [
      { title: '禁止政治与 R18 内容', description: '不讨论政治，不发布、传播或求取 R18 相关内容与资源。' },
      { title: '拒绝低俗、下头和过度擦边的内容', description: '不恶意曲解角色关系，不进行恶意 OOC（脱离原作设定）的二创讨论，尤其是 NTR 等令人不适的题材。' },
      { title: '适度玩梗，禁止刷屏', description: '不要大量复读恶俗内容或刷屏玩梗，让其他制作人也能正常交流、浏览消息。' },
      { title: '少发鬼图', description: '少发猎奇、惊吓或其他容易令人不适的图片，照顾群友的观感。' },
    ],
  },
  {
    id: 'disputes', number: '03', shortTitle: '不挂人、不出警',
    kicker: 'LEAVE OUTSIDE DISPUTES OUTSIDE', title: '把交流留给偶像。',
    intro: '这里是大家交流偶像的地方，请不要把私人恩怨和外部争端带进群聊。',
    rules: [
      { title: '禁止任何形式的挂人', description: '不发挂人帖，不挂他人言论或私人恩怨，也不要截图挂人、“避雷”。私人矛盾请私下解决。' },
      { title: '禁止跨平台“出警”', description: '不要将其他平台的纠纷引入群内，也不要在群里组织跨平台执法。群聊不是处理外部纠纷的法庭。' },
    ],
  },
]
</script>

<style scoped>
.handbook { background: #f7f6f2; color: #192030; }
.page-width { max-width: 1160px; margin: 0 auto; padding: 0 32px; }
.eyebrow { font-family: 'JetBrains Mono', monospace; font-size: 10px; line-height: 1.8; letter-spacing: .16em; font-weight: 400; }
.handbook-hero { position: relative; overflow: hidden; color: #fff; background: #0c1020; }
.hero-grid { position: absolute; inset: 0; opacity: .2; background-image: linear-gradient(#8796b51c 1px, transparent 1px), linear-gradient(90deg, #8796b51c 1px, transparent 1px); background-size: 64px 64px; mask-image: linear-gradient(90deg, transparent, #000); }
.hero-content { position: relative; display: grid; grid-template-columns: 1.3fr 1fr; align-items: center; gap: 80px; padding-top: 68px; padding-bottom: 66px; }
.hero-copy > .eyebrow { color: #b4b9c7; display: flex; gap: 12px; align-items: center; }
.hero-copy > .eyebrow span { width: 6px; height: 6px; border-radius: 50%; background: #ffcc00; box-shadow: 0 0 14px #ffcc0055; flex-shrink: 0; }
h1 { margin-top: 23px; font-size: clamp(36px, 4.7vw, 58px); font-weight: 800; letter-spacing: -.045em; line-height: 1.3; }
h1 > span { color: #ffce35; }
.hero-description { margin-top: 18px; color: #a9afc0; font-size: 14px; letter-spacing: .04em; }
.hero-actions { display: flex; align-items: center; flex-wrap: wrap; gap: 24px; margin-top: 30px; }
.button { display: inline-flex; align-items: center; justify-content: center; gap: 22px; border-radius: 8px; padding: 13px 20px; font-size: 13px; font-weight: 800; transition: background .2s, transform .2s; }
.button:hover { transform: translateY(-2px); }
.button-gold { background: #ffce35; color: #111728; }
.button-gold:hover { background: #ffe17c; }
.hero-join { color: #d2d5de; font-size: 12px; display: inline-flex; gap: 12px; padding: 10px 0; }
.hero-join:hover { color: #ffce35; }
.office-note { position: relative; padding: 28px 0 28px 32px; border-left: 1px solid #ffffff25; }
.office-note > .eyebrow { color: #79849b; font-size: 9px; }
.office-motto { margin-top: 20px; font-size: 26px; line-height: 1.6; font-weight: 700; letter-spacing: .05em; }
.office-description { margin-top: 18px; max-width: 270px; color: #99a1b5; font-size: 13px; line-height: 1.9; }
.office-stamp { position: absolute; right: -6px; bottom: -33px; color: #ffffff07; pointer-events: none; font-family: 'Space Grotesk', sans-serif; text-align: center; }
.office-stamp span { display: block; font-size: 100px; font-weight: 700; letter-spacing: -.07em; line-height: 1; }
.office-stamp small { font-size: 10px; letter-spacing: .38em; }
.handbook-layout { display: grid; grid-template-columns: 218px minmax(0, 1fr); gap: 65px; padding-top: 60px; padding-bottom: 30px; }
.contents-inner { position: sticky; top: 100px; }
.contents .eyebrow { color: #8d918f; font-size: 10px; letter-spacing: .1em; }
.contents nav { display: flex; flex-direction: column; margin-top: 22px; }
.contents nav a { display: flex; gap: 15px; align-items: baseline; padding: 12px 0; font-size: 12px; font-weight: 700; color: #626c78; }
.contents nav a:hover { color: #192030; }
.contents nav span { font: 10px 'JetBrains Mono', monospace; color: #9c9f9e; }
.sidebar-note { border-top: 1px solid #dedfd9; padding-top: 23px; margin-top: 25px; font-size: 12px; color: #92958e; line-height: 1.9; }
.anchor-section { scroll-margin-top: 90px; }
.section-label { color: #8a7844; }
.handbook-body h2 { font-weight: 800; font-size: 25px; line-height: 1.5; letter-spacing: -.03em; }
.community-section h2, .guidelines-intro h2 { margin-top: 10px; }
.body-copy { color: #667078; line-height: 1.95; font-size: 14px; margin-top: 15px; }
.brand-list { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 10px; margin-top: 26px; }
.brand-list li { display: flex; align-items: center; gap: 9px; padding: 12px 11px; background: #fff; border: 1px solid #e8e7e1; border-radius: 6px; font-size: 11px; color: #616976; }
.brand-code { font: 700 10px 'Space Grotesk', sans-serif; color: var(--brand-color); min-width: 32px; }
.guidelines-intro { margin-top: 48px; padding-top: 35px; border-top: 1px solid #dedfd9; }
.quick-rules { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 20px; }
.quick-rules span { background: #eeece4; color: #746744; font-size: 11px; padding: 7px 10px; border-radius: 4px; }
.rule-section { margin-top: 38px; padding-top: 32px; border-top: 1px solid #dedfd9; }
.rule-heading { display: flex; align-items: center; gap: 20px; }
.section-number { font: 500 42px 'Space Grotesk', sans-serif; line-height: 1; letter-spacing: -.06em; color: #c5c8be; }
.rule-heading .eyebrow { font-size: 9px; letter-spacing: .1em; margin-bottom: 5px; }
.rule-heading h2 { font-size: 23px; }
.section-intro { margin-top: 18px; color: #727b80; font-size: 13px; line-height: 1.9; }
.rule-list { display: flex; flex-direction: column; gap: 23px; padding: 25px 0 0; }
.rule-list li { display: flex; gap: 14px; align-items: flex-start; }
.rule-dot { width: 5px; height: 5px; flex-shrink: 0; border-radius: 50%; background: #b09c54; margin-top: 9px; }
.rule-list h3 { font-size: 14px; font-weight: 800; line-height: 1.7; }
.rule-list p { margin-top: 5px; font-size: 13px; color: #707881; line-height: 1.95; }
.moderation { display: flex; gap: 19px; align-items: flex-start; margin-top: 40px; padding: 26px; border: 1px solid #e7dfc4; background: #f1edde; border-radius: 8px; }
.moderation-symbol { flex-shrink: 0; width: 30px; height: 30px; border: 1px solid #c2ae69; color: #8a7130; border-radius: 50%; display: grid; place-items: center; font: 500 19px 'Space Grotesk', sans-serif; }
.moderation .eyebrow { font-size: 9px; color: #9e8b53; }
.moderation h2 { font-size: 17px; margin-top: 4px; }
.moderation p:not(.eyebrow) { color: #847958; font-size: 12px; line-height: 1.9; margin-top: 9px; }
.moderation-actions { display: flex; gap: 15px; margin-top: 16px; font-size: 12px; font-weight: 700; color: #7a652b; }
.moderation-actions i { font-style: normal; color: #c8ba8f; }
.join-section { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 280px); gap: 27px; align-items: center; padding-top: 50px; margin-top: 15px; }
.join-copy h2 { font-size: 27px; margin-top: 13px; }
.join-copy .body-copy { font-size: 13px; }
.qr-card { background: white; border: 1px solid #e4e7e6; padding: 15px; border-radius: 12px; text-align: center; box-shadow: 0 6px 24px #142a3510; }
.qr-trigger { display: block; width: 100%; cursor: zoom-in; border-radius: 5px; }
.qr-crop { display: block; position: relative; width: 100%; aspect-ratio: 1; overflow: hidden; border-radius: 5px; background: #f8f8fa; }
/* Show the actual QR with its quiet zone, rather than shrinking the full poster. */
.qr-crop img { position: absolute; width: 133.75%; height: auto; max-width: none; left: -16.6667%; top: -88.5417%; }
.qr-caption { display: flex; justify-content: center; gap: 16px; color: #617078; font-size: 11px; padding: 14px 0 8px; }
.original-link { display: inline-block; font-size: 11px; color: #8b969c; padding: 7px; text-decoration: underline; text-underline-offset: 3px; }
.original-link:hover { color: #182735; }
.closing-note { color: #999c92; font-size: 11px; line-height: 1.8; margin-top: 35px; text-align: center; border-top: 1px solid #dedfd9; padding: 25px 0 15px; }
.qr-dialog { width: min(640px, calc(100vw - 28px)); max-width: none; max-height: calc(100dvh - 28px); margin: auto; padding: 0; border: 0; border-radius: 16px; color: #192030; background: white; box-shadow: 0 30px 120px #0006; }
.qr-dialog::backdrop { background: #070b18cf; backdrop-filter: blur(6px); }
.qr-dialog-content { padding: 25px 28px; }
.qr-dialog-heading { display: flex; align-items: center; justify-content: space-between; gap: 10px; }
.qr-dialog-heading .eyebrow { font-size: 9px; }
.qr-dialog h2 { font-size: 19px; font-weight: 800; margin-top: 5px; }
.dialog-close { flex-shrink: 0; display: grid; place-items: center; width: 36px; height: 36px; border-radius: 50%; background: #f0f2f3; color: #63717c; font-size: 24px; }
.dialog-close:hover { background: #e3e8eb; }
.qr-large { width: min(100%, 480px, 52dvh); margin: 22px auto 0; }
.dialog-description { text-align: center; color: #78848c; font-size: 12px; margin-top: 18px; line-height: 1.8; }
.dialog-actions { display: flex; justify-content: center; align-items: center; flex-wrap: wrap; gap: 22px; margin-top: 22px; }
.button-dark { background: #172331; color: white; font-size: 12px; padding: 11px 17px; }
.button-dark:hover { background: #293f50; }
.download-link { font-size: 12px; color: #647681; text-decoration: underline; text-underline-offset: 4px; padding: 9px 0; }
a:focus-visible, button:focus-visible { outline: 3px solid #b59a35; outline-offset: 5px; }
@media (min-width: 1280px) { .join-section { grid-template-columns: minmax(0, 1fr) 310px; } }
@media (max-width: 900px) {
  .hero-content { gap: 30px; }
  .office-note { padding-left: 23px; }
  .office-motto { font-size: 22px; }
  .handbook-layout { grid-template-columns: 165px minmax(0, 1fr); gap: 32px; }
  .brand-list { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .join-section { grid-template-columns: 1fr; }
  .qr-card { width: min(100%, 340px); }
}
@media (max-width: 640px) {
  .page-width { padding-left: 22px; padding-right: 22px; }
  .hero-content { grid-template-columns: 1fr; gap: 30px; padding-top: 40px; padding-bottom: 38px; }
  .hero-copy > .eyebrow { font-size: 8px; letter-spacing: .08em; gap: 9px; }
  h1 { margin-top: 20px; font-size: 40px; }
  .hero-description { font-size: 12px; margin-top: 15px; }
  .hero-actions { gap: 20px; margin-top: 25px; }
  .button { font-size: 12px; gap: 14px; padding: 12px 16px; }
  .hero-join { font-size: 11px; gap: 7px; }
  .office-note { padding: 22px 0 0; border-left: 0; border-top: 1px solid #ffffff20; }
  .office-note > .eyebrow { font-size: 8px; }
  .office-motto { margin-top: 9px; font-size: 18px; }
  .office-motto br { display: none; }
  .office-description { font-size: 12px; margin-top: 8px; max-width: 280px; }
  .office-stamp { bottom: 0; right: 0; }
  .office-stamp span { font-size: 75px; }
  .handbook-layout { display: block; padding-top: 28px; }
  .contents-inner { position: static; }
  .contents nav { flex-direction: row; flex-wrap: wrap; gap: 8px 16px; margin-top: 10px; padding-bottom: 22px; border-bottom: 1px solid #dedfd9; }
  .contents nav a { gap: 7px; font-size: 11px; padding: 5px 0; }
  .sidebar-note { display: none; }
  .handbook-body { padding-top: 30px; }
  .handbook-body h2 { font-size: 23px; }
  .body-copy { font-size: 13px; }
  .brand-list { gap: 8px; margin-top: 20px; }
  .brand-list li { padding: 11px 9px; font-size: 10px; gap: 6px; }
  .brand-code { min-width: 31px; font-size: 10px; }
  .guidelines-intro { margin-top: 32px; padding-top: 28px; }
  .quick-rules { gap: 7px; }
  .quick-rules span { font-size: 10px; padding: 7px 8px; }
  .rule-heading { gap: 15px; }
  .section-number { font-size: 35px; }
  .rule-heading .eyebrow { font-size: 8px; letter-spacing: .05em; }
  .rule-heading h2 { font-size: 21px; }
  .rule-section { margin-top: 30px; padding-top: 26px; }
  .rule-list { gap: 20px; }
  .rule-list h3 { font-size: 13px; }
  .rule-list p { font-size: 12px; line-height: 2; }
  .moderation { gap: 13px; padding: 20px 16px; }
  .moderation h2 { font-size: 16px; }
  .join-section { gap: 20px; padding-top: 35px; }
  .join-copy h2 { font-size: 26px; }
  .qr-card { justify-self: center; }
  .qr-dialog-content { padding: 20px 18px; }
  .qr-dialog h2 { font-size: 17px; }
  .qr-dialog-heading .eyebrow { font-size: 8px; }
  .qr-large { margin-top: 18px; }
  .dialog-actions { gap: 18px; margin-top: 18px; }
}
@media (prefers-reduced-motion: reduce) { .button { transition: none; } .button:hover { transform: none; } }
</style>
