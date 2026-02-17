# SwiftID Platform Backend

SwiftID is a platform backend that simulates the core service layer of an online digital distribution and multiplayer system.  
The project implements user authentication, digital ownership licensing, presence tracking, and real-time matchmaking using REST APIs and WebSockets.

The goal of this project is to demonstrate backend engineering concepts such as client-server architecture, authentication, database design, and stateful real-time communication.

---

## Features

### Authentication Service
- User registration and login
- Secure password hashing
- JSON Web Token (JWT) authentication
- Protected API endpoints

### User Presence
- Online / offline user status
- Last-seen timestamps
- Online user lookup endpoint

### Digital Ownership (Entitlements)
- Product catalog
- Purchase system
- Ownership tracking
- User library retrieval

### Real-Time Lobby
- Persistent WebSocket connections
- Token-authenticated socket sessions
- Lobby room management
- Server-pushed events

### Matchmaking System
- Player matchmaking queue
- Automatic match grouping
- Dynamic match room creation
- Multi-client synchronization

---

## Tech Stack

- **Language:** Python
- **Framework:** Flask
- **Database:** PostgreSQL
- **Authentication:** JWT (PyJWT)
- **Real-Time:** Flask-SocketIO (WebSockets)
- **Client Testing:** Python Socket.IO Client
- **Version Control:** Git & GitHub

---

## System Architecture

The platform is organized into multiple backend services:

Client → REST API → Database  
Client → WebSocket → Real-Time Matchmaking Server

### Services
- **Identity Service** — user accounts and tokens
- **API Gateway** — protected routes
- **Entitlement Service** — digital ownership tracking
- **Presence Service** — online users
- **Real-Time Gateway** — socket connections
- **Matchmaking Service** — player coordination

The server is **authoritative**, meaning the server — not the client — determines match creation.

---

## Database Schema

### Users
Stores account credentials and presence state.

### Products
Digital items available for ownership.

### User Licenses
Tracks which users own which products (entitlements).

This mirrors how real platforms verify ownership before allowing access to content.

---

## API Endpoints

### Authentication

POST /auth/register
POST /auth/login
POST /auth/logout

### Users

GET /users/me
GET /users/online


### Store

POST /store/products
POST /store/purchase
GET /store/library


---

## WebSocket Events

| Event | Description |
|------|------|
| connect | Client connects to server |
| authenticate | Client authenticates using JWT |
| join_lobby | Joins shared lobby |
| find_match | Enters matchmaking queue |
| match_found | Server assigns match |
| disconnect | Client disconnects |

---

## Running the Project

### 1. Clone the repository

git clone https://github.com/cshamburger/swiftid-platform-backend.git
cd swiftid-platform-backend


### 2. Create a virtual environment

python -m venv venv
source venv/bin/activate


### 3. Install dependencies

pip install -r requirements.txt


### 4. Configure environment variables

Create a `.env` file:
SECRET_KEY=your_secret_key
DB_NAME=swiftid_db
DB_USER=your_db_user
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=5432


### 5. Create database
Make sure PostgreSQL is running, then:
createdb swiftid_db


### 6. Run the server
python app.py


Server will start at:
http://127.0.0.1:5000


---

## Testing Real-Time Matchmaking

Open two terminals and run:
python socket_test.py
python socket_test_2.py


When two authenticated users connect, the server automatically creates a match and notifies both clients.

---

## Concepts Demonstrated

- REST API design
- JWT authentication
- Authorization
- Relational database modeling
- Client-server architecture
- Persistent connections
- WebSockets
- Stateful server coordination
- Multiplayer matchmaking logic

---

## Future Improvements

- Persistent match storage
- Reconnect to active match
- Chat messaging
- Friend system
- Horizontal scaling (Redis pub/sub)
- Cloud deployment

---

## Author

**Corey Shamburger**  
https://github.com/cshamburger
