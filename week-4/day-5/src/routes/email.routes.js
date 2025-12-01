import { Router } from "express";
import { addEmailJob } from "../jobs/email.job.js";

const router = Router();

router.post("/send-email", async (req, res) => {
  const { to, subject, text } = req.body;

  if (!to || !subject || !text) {
    return res.status(400).json({ error: "to, subject & text are required" });
  }

  await addEmailJob({ to, subject, text });

  return res.json({ success: true, message: "Email queued" });
});

export default router;
