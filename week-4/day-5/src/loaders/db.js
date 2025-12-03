import mongoose from "mongoose";
import config from "../config/index.js";
import logger from "../utils/logger.js";

export default async function dbLoader() {
  try {
mongoose.connect(config.DB_URL, { autoIndex: process.env.NODE_ENV !== 'production' });
  } catch (err) {
    logger.error("DB Connection Error");
    logger.error(err);
    process.exit(1);
  }
}
