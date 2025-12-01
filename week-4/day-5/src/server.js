import appLoader from "./loaders/app.js";
import config from "./config/index.js";
import logger from "./utils/logger.js";

const start = async () => {
  const app = await appLoader();

  app.listen(config.PORT, () => {
    logger.info(`✔ Server started on port ${config.PORT}`);
  });
};

start();
