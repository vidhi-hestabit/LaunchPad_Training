import { Queue } from "bullmq";
import IORedis from "ioredis";

const connection = new IORedis({
  host: "127.0.0.1",
  maxRetriesPerRequest: null,
  port: 6379,
});

export const emailQueue = new Queue("emailQueue", { connection });

export const addEmailJob = async ({ to, subject, text }) => {
  return emailQueue.add(
    "sendEmail",
    { to, subject, text },
    {
      attempts: 3,
      backoff: { type: "exponential", delay: 5000 },
      removeOnComplete: true,
      removeOnFail: false,
    }
  );
};
