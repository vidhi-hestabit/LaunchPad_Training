import { defineConfig } from 'eslint-define-config';
import prettierPlugin from 'eslint-plugin-prettier';

export default defineConfig([
  {
    // This part is for global settings
    files: ['**/*.js', '**/*.cjs', '**/*.mjs'],
    languageOptions: {
      ecmaVersion: 'latest',
      sourceType: 'module',
      globals: {
        console: 'readonly',  // Define any global variables if needed
      },
    },
    plugins: {
      prettier: prettierPlugin, // Ensure Prettier plugin is applied
    },
    rules: {
      'no-unused-vars': 'warn',
      'no-console': 'warn',
      'prettier/prettier': 'error',  // Apply Prettier errors
      semi: ['error', 'always'],
      quotes: ['error', 'single'],
    },
  },
  {
    // Specific settings for the `src/**/*.js` files
    files: ['src/**/*.js'],
    rules: {
      'no-console': 'off',  // Allow console in `src` files
    },
  },
]);
