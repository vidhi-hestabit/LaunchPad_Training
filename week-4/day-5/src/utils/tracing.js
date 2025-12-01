import { v4 as uuidv4 } from "uuid";

export const generateRequestId = () => uuidv4();

export const attachRequestId = (req, res, next) => {
  const requestId = req.headers["x-request-id"] || generateRequestId();
  req.requestId = requestId;
  res.setHeader("X-Request-ID", requestId);
  console.log(`Request ${req.requestId} received`);

  next();
};
