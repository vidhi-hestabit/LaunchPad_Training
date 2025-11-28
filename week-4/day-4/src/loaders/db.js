import mongoose from "mongoose";
import config from "../config/index.js";
import logger from "../utils/logger.js";

export default async function dbLoader() {
  try {
    await mongoose.connect(config.DB_URL);
  } catch (err) {
    logger.error("❌ DB Connection Error");
    logger.error(err);
    process.exit(1);
  }
}
