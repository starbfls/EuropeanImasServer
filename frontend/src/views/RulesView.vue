<template>
  <div class="max-w-4xl mx-auto px-4 py-12">
    <h1 class="text-3xl font-extrabold text-gray-900 mb-1">Rules & Group Links</h1>
    <p class="text-gray-500 mb-10">Please read our community guidelines before participating.</p>

    <!-- CTA Buttons -->
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-14">
      <a
        href="#"
        class="group flex items-center gap-5 bg-indigo-600 hover:bg-indigo-700 text-white rounded-2xl p-6 shadow-lg transition-all duration-200 hover:-translate-y-1 hover:shadow-xl"
      >
        <span class="text-5xl select-none">💬</span>
        <div>
          <p class="text-xs uppercase font-bold text-indigo-300 mb-0.5 tracking-wider">Chat with us on</p>
          <p class="text-xl font-extrabold leading-tight">Discord Server</p>
          <p class="text-xs text-indigo-300 mt-1">Click to join the European iMas Discord</p>
        </div>
      </a>
      <a
        href="#"
        class="group flex items-center gap-5 bg-sky-500 hover:bg-sky-600 text-white rounded-2xl p-6 shadow-lg transition-all duration-200 hover:-translate-y-1 hover:shadow-xl"
      >
        <span class="text-5xl select-none">🐧</span>
        <div>
          <p class="text-xs uppercase font-bold text-sky-200 mb-0.5 tracking-wider">Join us on</p>
          <p class="text-xl font-extrabold leading-tight">QQ Group</p>
          <p class="text-xs text-sky-200 mt-1">欧洲偶像大师制作人群</p>
        </div>
      </a>
    </div>

    <!-- Rules sections -->
    <div class="space-y-6">
      <div
        v-for="(section, i) in rules"
        :key="i"
        class="bg-white rounded-2xl shadow-md p-6 border-l-4"
        :class="section.borderColor"
      >
        <h2 class="text-lg font-extrabold text-gray-900 mb-5 flex items-center gap-2.5">
          <span class="text-2xl">{{ section.icon }}</span>
          {{ section.title }}
        </h2>
        <ol class="space-y-3">
          <li
            v-for="(rule, j) in section.items"
            :key="j"
            class="flex items-start gap-3 text-gray-600 text-sm"
          >
            <span class="mt-0.5 text-xs font-extrabold text-gray-300 w-4 shrink-0">{{ j + 1 }}.</span>
            <span>{{ rule }}</span>
          </li>
        </ol>
      </div>
    </div>

    <!-- Footer note -->
    <p class="mt-10 text-center text-xs text-gray-400">
      By participating in this community, you agree to abide by these guidelines. Rules may be updated — check back occasionally.
    </p>
  </div>
</template>

<script setup>
const rules = [
  {
    icon: '🤝',
    title: 'General Conduct',
    borderColor: 'border-sky-400',
    items: [
      'Be respectful and welcoming to all members regardless of background, nationality, or preferred iMas branch.',
      'No harassment, bullying, or hate speech of any kind. This community is for everyone.',
      'Keep discussions civil — healthy debate is welcome, personal attacks are not.',
      'Respect the privacy of other members. Do not share personal information without explicit consent.',
    ],
  },
  {
    icon: '🎵',
    title: 'Content Guidelines',
    borderColor: 'border-purple-400',
    items: [
      'Keep content relevant to iDOLM@STER and related fan community activities.',
      'No piracy — do not share illegal streams, ripped files, or unauthorized game content.',
      'Fan art must credit the original creator. Do not claim others\' work as your own.',
      'NSFW content is strictly prohibited. This is a general-audience community.',
    ],
  },
  {
    icon: '📅',
    title: 'Events & Meetups',
    borderColor: 'border-green-400',
    items: [
      'RSVP for offline meetups in advance so organizers can plan appropriately.',
      'If you cannot attend after RSVPing, please cancel as early as possible.',
      'At in-person events, be mindful of public spaces and fellow attendees.',
      'Photos of members at events require their consent before being shared publicly.',
    ],
  },
  {
    icon: '⚠️',
    title: 'Enforcement',
    borderColor: 'border-amber-400',
    items: [
      'Moderators may warn, mute, kick, or ban members for violations depending on severity.',
      'First-time minor violations typically result in a formal warning.',
      'Repeated violations or severe misconduct may result in immediate and permanent removal.',
      'If you witness rule violations, please report them to a moderator rather than engaging directly.',
    ],
  },
]
</script>
