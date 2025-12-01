import nodemailer from "nodemailer";
import config from "../config/index.js";

export default async function sendEmail({ to, subject, text }) {
  if (!config.MAIL_USER || !config.MAIL_PASS) {
    throw new Error("⚠️ MAIL_USER or MAIL_PASS not defined in environment");
  }

  const transporter = nodemailer.createTransport({
    service: "gmail",
    auth: {
      user: config.MAIL_USER,
      pass: config.MAIL_PASS,
    },
  });

  return transporter.sendMail({
    from: config.MAIL_USER,
    to,
    subject,
    text,
  });
}
