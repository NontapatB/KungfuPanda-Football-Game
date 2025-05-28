# OptimalFlow Backend Developer Exercise

Thank you for giving me the opportunity to be tested.

This is a backend API built with **Node.js (Express)** that simulates a basic user system for testing backend knowledge. Data is stored in a simple file-based JSON format (`users.json`), and JWT is used for authentication.

## Features

- Register new users with hashed passwords
- Login and receive JWT token
- View all users (without password)
- Transfer balance between users
- Protected endpoints using JWT
- Integration tests using Jest + Supertest
- Docker support

---

## Project Structure

```
.
├── app.js                   # Main Express app
├── controllers/            # Route handlers (controllers)
├── services/               # Business logic (userService.js)
├── middleware/             # JWT Auth middleware
├── data/users.json         # Data storage file
├── tests/app.test.js       # Integration test
├── Dockerfile              # For containerizing the app
├── docker-compose.yml      # For running with Docker
├── .env                    # Environment variables
```

---

## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/NontapatB/optimalflow-backend-exercise.git
cd optimalflow-backend
```

### 2. Install dependencies
```bash
npm install
```

### 3. Create `.env` file
```env
JWT_SECRET=YOUROWN_SECRET_KEY
JWT_EXPIRES_IN=1h
PORT=3000
```

---

## Run Tests

```bash
npm test
```

Test covers full user flow:
- Register
- Login
- Transfer balance (with token)

---

## Run with Docker

### 1. Build & Run the container
```bash
docker-compose up --build
```

App will be available at:  
```
http://localhost:3000
```

### 2. Stop Docker
```bash
docker-compose down
```

---

## API Endpoints

Here 

| Method | Endpoint       | Description                 |
|--------|----------------|-----------------------------|
| POST   | `/users`       | Register new user           |
| POST   | `/login`       | Login and get JWT token     |
| GET    | `/users`       | Get all users               |
| POST   | `/transfer`    | Transfer balance (protected)|

> Protected routes require header:  
> `Authorization: Bearer <token>`

---

## API Testing with Postman

You can test the API using Postman by importing the collection from Backend-Exercise-API.postman_collection.json file

Alternatively, here is a preview of how the collection looks in Postman


Add User method post path /user

![image](https://github.com/user-attachments/assets/7d7255f3-c312-467e-9529-dd6fb9e2d637)

response

![image](https://github.com/user-attachments/assets/e091dc93-4cc2-4d43-a340-47ff11a80abc)



Add another User method post path /user

![image](https://github.com/user-attachments/assets/706215af-80a1-4ef6-93aa-9f3028f8273e)

response

![image](https://github.com/user-attachments/assets/c075dc0c-bcbd-401c-9d73-74bf5df139e3)



User login method post path /login

![image](https://github.com/user-attachments/assets/788defea-5d52-4a8c-bf5a-951c2a25ca0a)

reponse

![image](https://github.com/user-attachments/assets/f22b77e3-6ba2-43c3-8ca3-fd0288e43f89)



Get all users method get path /users

![image](https://github.com/user-attachments/assets/6de46f6e-a2b0-4e2c-97cb-2032a47e5a8a)

response

![image](https://github.com/user-attachments/assets/67448174-f8d6-49b7-b7f4-1b13b24e1cb6)



Get user by id method get path /users/:id

![image](https://github.com/user-attachments/assets/18e7b061-d834-4c87-9080-d5732dda3a5b)

response

![image](https://github.com/user-attachments/assets/5437b857-60ec-4000-812f-92875dd3b349)



Transfer balance between user with token method post path /transfer

![image](https://github.com/user-attachments/assets/5ad7038b-29fe-46d8-b5ca-a039c1b5ddf4)

![image](https://github.com/user-attachments/assets/fa161e8f-328b-4be5-938a-ff8a6b99b00e)

response

![image](https://github.com/user-attachments/assets/2f487a36-3c48-4e8c-97c8-ab25c726f3b7)

---

## About This Project

This is an exercise project created as part of a backend developer application process.  
**File-based storage** was used instead of databases for simplicity and testing focus.

---

###  Scalability Plan: Handling 10x Traffic

If this system needs to handle 10 times more users or traffic, it’s a good idea to use Docker along with load balancing and a container orchestration tool like Kubernetes, so the app can run multiple instances at the same time. For frequently accessed data, like the user list, adding a cache layer can help reduce server load. It’s also important to implement rate limiting to protect against traffic spikes or abuse, and to set up monitoring tools to keep track of the system’s health in real time. For tasks that take longer to complete, like sending emails or writing logs, you can offload them to a background queue using a tool like RabbitMQ. All of these changes will help ensure the system stays reliable and responsive even under much heavier usage.

##  Author

Developed by [Nontapat](https://github.com/NontapatB)

