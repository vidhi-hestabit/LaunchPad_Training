import helmet from "helmet";
import cors from "cors";
import rateLimit from "express-rate-limit";
import express from "express";
import hpp from "hpp";
import xss from "xss";

// Prevent NoSQL injection
export const sanitizeNoSQL = (req, res, next) => {
  const clean = (obj) => {
    if (!obj || typeof obj !== "object") return;
    for (const key in obj) {
      if (key.startsWith("$")) delete obj[key];
      if (typeof obj[key] === "object") clean(obj[key]);
    }
  };
  clean(req.body);
  clean(req.query);
  clean(req.params);
  next();
};

// Prevent XSS (run AFTER validation)
export const sanitizeXSS = (req, res, next) => {
  const clean = (obj) => {
    if (!obj || typeof obj !== "object") return;
    for (const key in obj) {
      if (typeof obj[key] === "string") {
        obj[key] = xss(obj[key]);
      } else if (typeof obj[key] === "object") {
        clean(obj[key]);
      }
    }
  };
  clean(req.body);
  clean(req.query);
  clean(req.params);
  next();
};

// Apply global security middlewares
export const applySecurityMiddlewares = (app) => {
  app.use(express.json({ limit: "10kb" }));

  app.use(helmet());

  app.use(cors({
    origin: ["http://localhost:3000", "http://localhost:3001"],
    methods: ["GET", "POST", "PUT", "DELETE", "PATCH"],
    allowedHeaders: ["Content-Type", "Authorization"],
    credentials: true
  }));

  app.use(rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes per IP
    max: 100,
    message: {
      success: false,
      error: "Too many requests"
    }
  }));

  app.use(hpp());
  app.use(sanitizeNoSQL);
};
