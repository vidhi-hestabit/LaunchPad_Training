import dotenv from "dotenv";
import fs from "fs";
import path from "path";

const env = process.env.NODE_ENV || "local";
const envFile = `.env.${env}`;
const envPath = path.resolve(process.cwd(), envFile);

if (fs.existsSync(envPath)) {
  dotenv.config({ path: envPath });
} else {
  console.warn(`⚠️ Environment file ${envFile} not found`);
}

export default {
  PORT: process.env.PORT,
  DB_URL: process.env.DB_URL,
};

