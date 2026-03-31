<div align="center">

<br/>

```
 ██████╗██╗     ███████╗ █████╗ ███╗   ██╗ ██████╗ ██████╗ ███╗   ██╗███╗   ██╗███████╗ ██████╗████████╗
██╔════╝██║     ██╔════╝██╔══██╗████╗  ██║██╔════╝██╔═══██╗████╗  ██║████╗  ██║██╔════╝██╔════╝╚══██╔══╝
██║     ██║     █████╗  ███████║██╔██╗ ██║██║     ██║   ██║██╔██╗ ██║██╔██╗ ██║█████╗  ██║        ██║   
██║     ██║     ██╔══╝  ██╔══██║██║╚██╗██║██║     ██║   ██║██║╚██╗██║██║╚██╗██║██╔══╝  ██║        ██║   
╚██████╗███████╗███████╗██║  ██║██║ ╚████║╚██████╗╚██████╔╝██║ ╚████║██║ ╚████║███████╗╚██████╗   ██║   
 ╚═════╝╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═══╝╚══════╝ ╚═════╝   ╚═╝  
```

### 🧹 *Connecting People with Professional Cleaning Services — Seamlessly.*

<br/>

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.129-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)](https://sqlalchemy.org)
[![JWT](https://img.shields.io/badge/JWT-Auth-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white)](https://jwt.io)
[![HTML5](https://img.shields.io/badge/HTML5-Frontend-E34F26?style=for-the-badge&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

<br/>

---

</div>

## 📖 What is CleanConnect?

**CleanConnect** is a full-stack web platform designed to bridge the gap between households and professional cleaning service providers. In an era where convenience is king, CleanConnect eliminates the friction of finding, vetting, and booking cleaning professionals — all through a clean, intuitive interface backed by a secure, high-performance API.

> 🎯 **Mission:** Make professional cleaning services accessible, trustworthy, and effortless for every home and business.

Whether you're a busy professional who needs weekly home cleaning, a property manager coordinating services across multiple locations, or a cleaning business looking to reach more clients — **CleanConnect is the platform that brings everyone together.**

### 🌟 The Problem We Solve

```
  BEFORE CleanConnect                      AFTER CleanConnect
  ─────────────────────────────────────    ──────────────────────────────────────
  📞 Endless phone calls & no-shows   →   ✅ Book instantly through the platform
  ❓ Unknown service quality           →   ⭐ Verified providers with track records
  📋 Manual paperwork & invoices       →   📊 Auto-generated reports & history
  🔓 No secure user accounts           →   🔐 JWT-secured authentication system
  🗓️ Scheduling conflicts              →   📅 Streamlined booking management
```

---

## ✨ Key Features

<table>
<tr>
<td width="50%">

### 🔐 Secure Authentication
- User registration & login
- JWT token-based sessions
- Argon2 password hashing (industry standard)
- Protected API endpoints
- Token validation middleware

</td>
<td width="50%">

### 📊 Reports & Analytics
- Service history tracking
- Automated report generation
- Booking and activity logs
- Data persistence via SQLAlchemy
- Exportable records

</td>
</tr>
<tr>
<td width="50%">

### ⚡ High-Performance API
- FastAPI framework (async-ready)
- Interactive Swagger docs at `/docs`
- Pydantic data validation
- RESTful endpoint design
- Uvicorn ASGI server

</td>
<td width="50%">

### 🌐 Clean Frontend
- HTML5 & CSS3 interface
- Intuitive booking forms
- Responsive design
- Direct API integration
- Lightweight & fast-loading

</td>
</tr>
</table>

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         CleanConnect Platform                        │
│                                                                       │
│   ┌─────────────────────┐         ┌───────────────────────────────┐  │
│   │     FRONTEND        │         │          BACKEND (API)        │  │
│   │  ─────────────────  │         │  ───────────────────────────  │  │
│   │                     │  HTTP   │                               │  │
│   │  📄 HTML Pages      │◄───────►│  ⚡ FastAPI Application       │  │
│   │  🎨 CSS Styles      │  REST   │  🔀 Route Handlers            │  │
│   │  📋 Booking Forms   │         │  🛡️  Auth Middleware          │  │
│   │  👤 User Interface  │         │                               │  │
│   └─────────────────────┘         └──────────────┬────────────────┘  │
│                                                   │                   │
│                          ┌────────────────────────┼──────────────┐   │
│                          │                        │              │   │
│                   ┌──────▼──────┐         ┌───────▼──────┐      │   │
│                   │   AUTH      │         │   REPORTS    │      │   │
│                   │  MODULE     │         │   MODULE     │      │   │
│                   │  ─────────  │         │  ──────────  │      │   │
│                   │ 🔑 Register │         │ 📊 Generate  │      │   │
│                   │ 🔓 Login    │         │ 📋 Retrieve  │      │   │
│                   │ 🎟️ JWT      │         │ 💾 Store     │      │   │
│                   └──────┬──────┘         └───────┬──────┘      │   │
│                          │                        │              │   │
│                          └───────────┬────────────┘              │   │
│                                      │                           │   │
│                              ┌───────▼────────┐                  │   │
│                              │   DATABASE     │                  │   │
│                              │   (SQLite /    │                  │   │
│                              │   PostgreSQL)  │                  │   │
│                              │  ────────────  │                  │   │
│                              │  👥 Users      │                  │   │
│                              │  📋 Reports    │                  │   │
│                              │  📅 Bookings   │                  │   │
│                              └────────────────┘                  │   │
└──────────────────────────────────────────────────────────────────┘
```

---

## 🔄 User Authentication Flow

```
   Client                   FastAPI                  Database
     │                         │                         │
     │  POST /auth/register    │                         │
     │────────────────────────►│                         │
     │  { email, password }    │   Hash password         │
     │                         │   (Argon2)              │
     │                         │──── INSERT user ───────►│
     │                         │◄──── user_id ───────────│
     │◄────────────────────────│                         │
     │   { message: "ok" }     │                         │
     │                         │                         │
     │  POST /auth/login       │                         │
     │────────────────────────►│                         │
     │  { email, password }    │──── SELECT user ───────►│
     │                         │◄──── user record ───────│
     │                         │   Verify hash           │
     │                         │   Generate JWT          │
     │◄────────────────────────│                         │
     │   { access_token }      │                         │
     │                         │                         │
     │  GET /reports           │                         │
     │  Authorization: Bearer  │                         │
     │────────────────────────►│                         │
     │                         │   Validate JWT          │
     │                         │   Decode payload        │
     │                         │──── SELECT reports ────►│
     │◄────────────────────────│◄──── data ──────────────│
     │   { reports: [...] }    │                         │
```

---

## 📁 Project Structure

```
CleanConnect/
│
├── 📂 backend/                    # Python FastAPI application
│   ├── 📂 authentication/         # Auth module
│   │   ├── 🐍 models.py           #   User data models (SQLAlchemy)
│   │   ├── 🐍 routes.py           #   /register & /login endpoints
│   │   ├── 🐍 schemas.py          #   Pydantic request/response schemas
│   │   └── 🐍 utils.py            #   JWT creation, password hashing
│   │
│   ├── 📂 reports/                # Reports module
│   │   ├── 🐍 models.py           #   Report data models
│   │   ├── 🐍 routes.py           #   CRUD endpoints for reports
│   │   └── 🐍 schemas.py          #   Report schemas
│   │
│   ├── 🐍 database.py             # DB engine & session factory
│   ├── 🐍 main.py                 # App entry point, router registration
│   └── 🐍 __init__.py
│
├── 📂 frontend/                   # HTML/CSS user interface
│   ├── 🌐 index.html              #   Landing / home page
│   ├── 🌐 login.html              #   Login page
│   ├── 🌐 register.html           #   Registration page
│   ├── 🌐 dashboard.html          #   User dashboard
│   └── 🎨 styles.css             #   Global styles
│
├── 📄 requirements.txt            # Python dependencies
├── 📄 .gitignore
└── 📄 README.md
```

---

## 🛠️ Tech Stack

<div align="center">

| Layer | Technology | Version | Purpose |
|:-----:|:----------:|:-------:|:-------:|
| 🚀 **Framework** | FastAPI | 0.129.2 | REST API & routing |
| 🗄️ **ORM** | SQLAlchemy | 2.0.46 | Database models & queries |
| ✅ **Validation** | Pydantic | 2.12.5 | Request/response schemas |
| 🔐 **Auth** | python-jose | 3.5.0 | JWT creation & verification |
| 🔒 **Hashing** | Passlib (Argon2) | 1.7.4 | Secure password hashing |
| 🌐 **Server** | Uvicorn | 0.41.0 | ASGI production server |
| 🔧 **Config** | python-dotenv | 1.2.1 | Environment variables |
| 📧 **Email** | email-validator | 2.3.0 | Input validation |
| 🎨 **Frontend** | HTML5 / CSS3 | — | User interface |

</div>

---

## 🚀 Getting Started

### Prerequisites

Make sure you have the following installed:

```
✅ Python 3.8 or higher
✅ pip (Python package manager)
✅ Git
```

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/aastha-9798/CleanConnect.git
cd CleanConnect
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Configure Environment

Create a `.env` file in the root directory:

```env
# .env
SECRET_KEY=your-super-secret-jwt-key-here
DATABASE_URL=sqlite:///./cleanconnect.db
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

> ⚠️ **Never commit your `.env` file** — it's already listed in `.gitignore`.

### 4️⃣ Run the Application

```bash
uvicorn backend.main:app --reload
```

You should see:

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process using StatReload
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### 5️⃣ Explore the API

| URL | Description |
|-----|-------------|
| `http://localhost:8000` | Application root |
| `http://localhost:8000/docs` | 📖 Interactive Swagger UI |
| `http://localhost:8000/redoc` | 📄 ReDoc documentation |

---

## 🔌 API Endpoints

```
╔══════════════════════════════════════════════════════════════╗
║                    CleanConnect REST API                      ║
╠══════════════╦══════════════════════╦════════════════════════╣
║ Method       ║ Endpoint             ║ Description            ║
╠══════════════╬══════════════════════╬════════════════════════╣
║ POST         ║ /auth/register       ║ Create new account     ║
║ POST         ║ /auth/login          ║ Login & get JWT token  ║
╠══════════════╬══════════════════════╬════════════════════════╣
║ GET          ║ /reports             ║ Fetch all reports 🔐   ║
║ POST         ║ /reports             ║ Create new report 🔐   ║
║ GET          ║ /reports/{id}        ║ Fetch report by ID 🔐  ║
║ DELETE       ║ /reports/{id}        ║ Delete a report 🔐     ║
╚══════════════╩══════════════════════╩════════════════════════╝
                                          🔐 = Requires JWT token
```

### Example: Register a User

```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123!"
  }'
```

### Example: Login & Get Token

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123!"
  }'

# Response:
# { "access_token": "eyJhbGci...", "token_type": "bearer" }
```

### Example: Access Protected Route

```bash
curl -X GET "http://localhost:8000/reports" \
  -H "Authorization: Bearer eyJhbGci..."
```

---

## 🔐 Security Design

```
  ┌─────────────────────────────────────────────────────┐
  │               Security Architecture                   │
  │                                                       │
  │  🔒 Password Storage                                  │
  │     Plain text  ────────X──────────►  NEVER stored   │
  │     Password    ──[ Argon2 Hash ]──►  Hash stored     │
  │                                                       │
  │  🎟️  JWT Token Structure                              │
  │     ┌───────────┬────────────────┬──────────────┐    │
  │     │  Header   │    Payload     │  Signature   │    │
  │     │ algorithm │  user_id       │  HMAC-SHA256 │    │
  │     │  HS256    │  expiry time   │  with SECRET │    │
  │     └───────────┴────────────────┴──────────────┘    │
  │                                                       │
  │  🛡️  Every protected route validates:                 │
  │     1. Token exists in Authorization header           │
  │     2. Signature is valid (not tampered)              │
  │     3. Token has not expired                          │
  │     4. User still exists in database                  │
  └─────────────────────────────────────────────────────┘
```

---

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

```bash
# 1. Fork the repository on GitHub

# 2. Clone your fork
git clone https://github.com/YOUR-USERNAME/CleanConnect.git

# 3. Create a feature branch
git checkout -b feature/your-amazing-feature

# 4. Make your changes and commit
git add .
git commit -m "✨ Add: your amazing feature"

# 5. Push to your fork
git push origin feature/your-amazing-feature

# 6. Open a Pull Request on GitHub
```

### Commit Message Convention

| Prefix | Use for |
|--------|---------|
| `✨ Add:` | New features |
| `🐛 Fix:` | Bug fixes |
| `📚 Docs:` | Documentation updates |
| `♻️ Refactor:` | Code refactoring |
| `🔒 Security:` | Security improvements |

---

## 📊 Project Stats

```
  Language Breakdown
  ──────────────────────────────────────────────
  HTML    ████████████████████████████░░░   86.6%
  Python  ████████░░░░░░░░░░░░░░░░░░░░░░░   11.3%
  CSS     ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░    2.1%
  ──────────────────────────────────────────────
```

---

## 🗺️ Roadmap

- [x] User authentication (register/login)
- [x] JWT-secured API endpoints
- [x] Reports module
- [x] HTML/CSS frontend
- [ ] 🔜 Service provider profiles
- [ ] 🔜 Booking & scheduling system
- [ ] 🔜 Payment integration
- [ ] 🔜 Review & rating system
- [ ] 🔜 Mobile-responsive redesign
- [ ] 🔜 Email notifications
- [ ] 🔜 Admin dashboard

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

Built with ❤️ by [**aastha-9798**](https://github.com/aastha-9798)

⭐ If you found this project helpful, please consider giving it a **star**!

[![GitHub stars](https://img.shields.io/github/stars/aastha-9798/CleanConnect?style=social)](https://github.com/aastha-9798/CleanConnect/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/aastha-9798/CleanConnect?style=social)](https://github.com/aastha-9798/CleanConnect/network/members)

</div>
