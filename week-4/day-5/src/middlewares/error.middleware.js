export default function errorHandler(err, req, res, next) {
  const code = err.code || "INTERNAL_SERVER_ERROR";
  const status = err.status || 500;

  res.status(status).json({
    success: false,
    message: err.message || "Something went wrong",
    code,
    timestamp: new Date().toISOString(),
    path: req.originalUrl,
  });
}
