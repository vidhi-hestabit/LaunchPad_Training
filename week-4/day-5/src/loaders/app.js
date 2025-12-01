import express from "express";
import morgan from "morgan";
import routes from "../routes/index.js";
import logger from "../utils/logger.js";
import dbLoader from "./db.js";
import { applySecurityMiddlewares } from "../middlewares/security.js";
import { attachRequestId } from "../utils/tracing.js";

export default async function appLoader() {
  const app = express();

  applySecurityMiddlewares(app);
  logger.info("Bootstrapping application...");

  app.use(attachRequestId);

  app.use((req, res, next) => {
    logger.info(`Incoming request: ${req.method} ${req.url}`, {
      requestId: req.requestId,
    });
    next();
  });

  await dbLoader();

  app.use(express.json());
  app.use(morgan("dev"));
  logger.info("Middlewares loaded");

  const routeCount = routes(app);
  logger.info(`Routes mounted: ${routeCount} endpoints`);

  return app;
}
