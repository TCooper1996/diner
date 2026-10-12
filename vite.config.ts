/// <reference types="vitest" />
import { defineConfig } from 'vite';
import { resolve } from 'path';

export default defineConfig({
  resolve: {
    alias: {
      '@core': resolve(__dirname, './src/core'),
      '@application': resolve(__dirname, './src/application'),
      '@actions': resolve(__dirname, './src/actions'),
      '@test_utils': resolve(__dirname, './src/test_utils')
    }
  },
  test: {
    globals: true,
    environment: 'node',
    include: ['src/**/*.test.ts']
  }
}); 