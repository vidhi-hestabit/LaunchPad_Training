npm init -y

npm install express dotenv mongoose
npm install winston pino pino-pretty
npm install cors morgan helmet compression


mkdir -p src/{config,loaders,models,routes,controllers,services,repositories,middlewares,utils,jobs,logs}

Main endpoint - route
![alt text](image.png)

Get all users Endpoint

![alt text](image-1.png)

Post user request 

{
    "firstName":"user1",
    "lastName":"last1",
    "email":"userlast1@gmail.com",
    "password":"098765",
    "status":"active"
}

![alt text](image-2.png)

Get user by ID 

![alt text](image-3.png)

Delete User

![alt text](image-4.png)

Get all products 

![alt text](image-5.png)

Post product request

![alt text](image-6.png)
