import dotenv from "dotenv";
import fs from "fs";
import path from "path";

const env = process.env.NODE_ENV || "local";
const envFile = `.env.${env}`;
const envPath = path.resolve(process.cwd(), envFile);


console.log("NODE_ENV =", env);
console.log("process.cwd() =", process.cwd());
console.log("Looking for env file at =", envPath);


if (fs.existsSync(envPath)) {
  dotenv.config({ path: envPath, override: true });
  console.log(`Loaded environment variables from ${envFile}`);
} else {
  console.warn(`Environment file ${envFile} not found`);
}

export default {
  PORT: process.env.PORT,
  DB_URL: process.env.DB_URL,
  REDIS_URL: process.env.REDIS_URL,
  MAIL_USER: process.env.MAIL_USER,
  MAIL_PASS: process.env.MAIL_PASS,
};
