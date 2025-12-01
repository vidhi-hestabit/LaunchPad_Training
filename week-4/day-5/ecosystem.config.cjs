module.exports = {
  apps: [
    {
      name: "api",
      script: "src/server.js",
      env: { NODE_ENV: "production" },
    },
    {
      name: "email-worker",
      script: "src/workers/email.worker.js",
      env: { NODE_ENV: "production" },
    },
  ],
};
