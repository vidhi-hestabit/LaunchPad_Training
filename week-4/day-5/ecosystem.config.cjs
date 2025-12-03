module.exports = {
  apps: [
    {
      name: "api",
      script: "./src/server.js",
      watch: false,
      env: {
        NODE_ENV: "dev",
        dotenv: "/home/vidhiajmera/launchpad/week-4/day-5/.env.dev",
      },
      env_production: {
        NODE_ENV: "production",
        dotenv: "/home/vidhiajmera/launchpad/week-4/day-5/.env.production",
      },
    },
    {
      name: "worker",
      script: "./src/workers/email.worker.js",
      watch: false,
      env: {
        NODE_ENV: "dev",
        dotenv: "/home/vidhiajmera/launchpad/week-4/day-5/.env.dev",
      },
      env_production: {
        NODE_ENV: "production",
        dotenv: "/home/vidhiajmera/launchpad/week-4/day-5/.env.production",
      },
    }
  ]
}
