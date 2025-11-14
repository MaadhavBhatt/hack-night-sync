<template>
  <div class="center">
    <h1 class="next">Next Hack Night in N minutes</h1>
  </div>
</template>

<script setup lang="ts">
import { createClient } from '@supabase/supabase-js'
import { ref, onMounted } from 'vue'

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL as string
const supabaseKey = import.meta.env.VITE_SUPABASE_KEY as string

if (!supabaseUrl || !supabaseKey) {
  console.warn('Supabase URL or Key is missing')
  throw new Error('Supabase URL or Key is not defined in environment variables')
}

const supabase = createClient(supabaseUrl, supabaseKey)

const loading = ref(true)
const error = ref<string | null>(null)
const minutes = ref<number | null>(null)
const title = ref<string | null>(null)

async function loadNextEvent() {
  loading.value = true
  error.value = null

  try {
    const nowIso = new Date().toISOString()

    // Fetch the next upcoming hack night event
    const { data, error: supaErr } = await supabase
      .from('hack_night_plans')
      .select('id, plan_title, start_time')
      .gt('start_time', nowIso)
      .order('start_time', { ascending: true })
      .limit(1)

    if (supaErr) throw supaErr

    if (!data || data.length === 0) {
      // No upcoming events
      console.log('No upcoming events found')
    } else {
      const nextEvent = data[0] as { id: number; plan_title: string; start_time: string }
      title.value = nextEvent.plan_title ?? 'Hack Night'
      const start = new Date(nextEvent.start_time)
      const diffMinutes = Math.max(0, Math.round((start.getTime() - Date.now()) / 60000))
      minutes.value = diffMinutes
    }
  } catch (err: any) {
    console.error('Error fetching next event:', err)
    error.value = err?.message ?? String(err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadNextEvent() // Initial load
  setInterval(loadNextEvent, 60000) // Refresh every minute
})
</script>

<style>
/* Import Google Sans Code font */
@import url('https://fonts.googleapis.com/css2?family=Google+Sans+Code:ital,wght@0,300..800;1,300..800&display=swap');

/* Do not use !important inside layers */
@layer reset, base, layout, components, utilities;

:root {
  --font-primary: 'Google Sans Code', monocode;
  --clr-black: #0a0a0a;
  --clr-white: #fefefe;
}

/* CSS Reset from https://www.joshwcomeau.com/css/custom-css-reset/ */
@layer reset {
  *,
  *::before,
  *::after {
    box-sizing: border-box;
  }

  * {
    margin: 0;
    padding: 0;
  }

  @media (prefers-reduced-motion: no-preference) {
    html {
      interpolate-size: allow-keywords;
    }
  }

  body {
    line-height: 1.5;
    -webkit-font-smoothing: antialiased;
  }

  img,
  picture,
  video,
  canvas,
  svg {
    display: block;
    max-width: 100%;
  }

  input,
  button,
  textarea,
  select {
    font: inherit;
  }

  p,
  h1,
  h2,
  h3,
  h4,
  h5,
  h6 {
    overflow-wrap: break-word;
  }

  p {
    text-wrap: pretty;
  }

  h1,
  h2,
  h3,
  h4,
  h5,
  h6 {
    text-wrap: balance;
  }

  #root,
  #__next {
    isolation: isolate;
  }

  :root {
    font-size: 10px;
  }
}

@layer base {
  body {
    font-family: var(--font-primary);
    color: var(--clr-white);
    background-color: var(--clr-black);
  }
}

@layer components {
  .next {
    font-size: 4rem;
    text-align: center;
  }
}

@layer utilities {
  .center {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
  }
}
</style>
