<template>
  <div class="center">
    <h1 class="next">Next Hack Night in N minutes</h1>
  </div>
</template>

<script setup lang="ts"></script>

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
