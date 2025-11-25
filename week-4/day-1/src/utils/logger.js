import winston from "winston";
import fs from "fs";
import path from "path";

// Ensure logs folder exists
const logDir = path.join(process.cwd(), "src/logs");
if (!fs.existsSync(logDir)) {
  fs.mkdirSync(logDir, { recursive: true });
}

const logger = winston.createLogger({
  level: "info",

  format: winston.format.combine(
    winston.format.timestamp({ format: "YYYY-MM-DD HH:mm:ss" }),
    winston.format.printf(
      (info) =>
        `[${info.timestamp}] ${info.level.toUpperCase()}: ${info.message}`
    )
  ),

  transports: [
    // 🔹 Console logs (colored)
    new winston.transports.Console({
      format: winston.format.combine(
        winston.format.colorize(),
        winston.format.timestamp({ format: "HH:mm:ss" }),
        winston.format.printf(
          (info) =>
            `[${info.timestamp}] ${info.level}: ${info.message}`
        )
      ),
    }),

    // 🔹 All logs here
    new winston.transports.File({
      filename: path.join(logDir, "app.log"),
      level: "info",
    }),

    // 🔹 Error logs separately
    new winston.transports.File({
      filename: path.join(logDir, "error.log"),
      level: "error",
    }),
  ],
});

// Ensure logger doesn't crash if no catch block exists
logger.stream = {
  write: (message) => logger.info(message.trim()),
};

export default logger;
