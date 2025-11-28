import express from "express";
import morgan from "morgan";
import routes from "../routes/index.js";
import logger from "../utils/logger.js";
import dbLoader from "./db.js";
import { applySecurityMiddlewares } from "../middlewares/security.js";



export default async function appLoader() {
  const app = express();
  applySecurityMiddlewares(app);

  logger.info("⏳ Bootstrapping application...");

  await dbLoader();
  logger.info("✔ Database connected");

  app.use(express.json());
  app.use(morgan("dev"));
  logger.info("✔ Middlewares loaded");

  const routeCount = routes(app);
  logger.info(`✔ Routes mounted: ${routeCount} endpoints`);

  return app;
}
