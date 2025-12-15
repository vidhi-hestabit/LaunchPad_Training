npm init -y

npm install express dotenv mongoose
npm install winston pino pino-pretty
npm install cors morgan helmet compression


mkdir -p src/{config,loaders,models,routes,controllers,services,repositories,middlewares,utils,jobs,logs}


npm install helmet cors express-rate-limit
npm i joi


npm install --save-dev jest supertest cross-env



npm install bullmq ioredis nodemailer


## Email worker:

![alt text](image-2.png)


## Sent Email:

![alt text](image-3.png)


### Access my postman endpoint collection here :-

https://vidhia-hestabit-2290414.postman.co/workspace/Vidhi-Ajmera's-Workspace~b629ae29-2d46-487a-859f-c51a8e4e94b8/collection/49847169-a2ca447e-614f-42b1-b27a-ccd367607ea1?action=share&source=copy-link&creator=49847169

App running :

 ![alt text](<Screenshot from 2025-11-26 18-05-38.png>) 
 

 Users endpoint :

 ![alt text](<Screenshot from 2025-11-26 18-06-54.png>) 
 

 Post user endpoint :

 ![alt text](<Screenshot from 2025-11-26 18-08-53.png>) 
 

 Get user by ID :
 
 ![alt text](<Screenshot from 2025-11-26 18-10-08.png>) 
 

 Delete User by ID :

 ![alt text](<Screenshot from 2025-11-26 18-11-09.png>) 
 

 Get all products :

 ![alt text](<Screenshot from 2025-11-26 18-12-28.png>) 
 
 Post product :
 
 ![alt text](<Screenshot from 2025-11-26 18-14-07.png>)

pm2 start src/server.js -name my-app

pm2 restart my-app

pm2 start ecosystem.config.cjs
