import { defineConfig } from 'eslint-define-config';
import prettierPlugin from 'eslint-plugin-prettier';

export default defineConfig([
  {
    languageOptions: {
      ecmaVersion: 'latest', // equivalent to parserOptions.ecmaVersion
      sourceType: 'module',  // If you're using ES modules
      globals: {
        console: 'readonly', // Define any global variables if needed
      },
    },
    plugins: {
      prettier: prettierPlugin, // Make sure the Prettier plugin is used
    },
    rules: {
      // ESLint recommended rules
      'no-unused-vars': 'warn',  // Example rule (from eslint:recommended)
      'no-console': 'warn',      // Example rule (from eslint:recommended)

      // Prettier's rules
      'prettier/prettier': 'error',  // Ensure Prettier errors are caught

      // Custom rules
      semi: ['error', 'always'],
      quotes: ['error', 'single'],
    },
  },
  {
    files: ['src/**/*.js'],
    rules: {
      'no-console': 'off',  // Allow console in your source files
    },
  },
]);
