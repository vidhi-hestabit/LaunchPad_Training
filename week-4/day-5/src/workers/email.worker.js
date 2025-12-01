import { Worker } from "bullmq";
import IORedis from "ioredis";
import sendEmail from "../services/email.service.js";

const connection = new IORedis({
  host: "127.0.0.1",
  maxRetriesPerRequest: null,
  port: 6379,
});

const worker = new Worker(
  "emailQueue",
  async (job) => {
    console.log("Processing job:", job.name, job.data);
    await sendEmail(job.data);
  },
  { connection }
);

worker.on("completed", (job) => {
  console.log(`Email job completed: ${job.id}`);
});

worker.on("failed", (job, err) => {
  console.error(`Email job failed: ${job.id}`, err);
});
