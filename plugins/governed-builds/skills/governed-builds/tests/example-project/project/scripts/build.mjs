import { mkdirSync, copyFileSync } from 'node:fs';
mkdirSync('dist', { recursive: true });
copyFileSync('src/slugify.mjs', 'dist/slugify.mjs');
console.log('build passed');
