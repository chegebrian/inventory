# 📦 Inventory Management System

A full-stack Inventory Management System built with **Flask (backend API)** and **React (frontend UI)**. This application allows users to manage inventory items, track stock levels, and perform CRUD operations efficiently.

---

## 🚀 Project Overview

This project is designed to demonstrate a **modern full-stack architecture**, separating concerns between:

- 🔧 Backend API (Flask)
- 🎨 Frontend UI (React + Tailwind CSS)

It can be used as:

- A portfolio project
- A starter template for inventory-based systems
- A learning resource for full-stack development

---

## 🧱 Project Structure

```
inventory/
│
├── server/        # Flask backend API
│   ├── run.py     # Entry point
│   ├── Procfile   # Deployment config
│   ├── runtime.txt
│   └── ...
│
├── client/        # React frontend
│   ├── src/
│   ├── public/
│   ├── tailwind.config.js
│   └── ...
│
└── README.md
```

---

## ⚙️ Tech Stack

### Backend

- Flask
- Flask REST API
- SQLAlchemy (ORM)
- Gunicorn (production server)

### Frontend

- React
- Tailwind CSS
- Fetch API

### Deployment

- Render
- Gunicorn

---

## 🔥 Features

- ✅ Create, Read, Update, Delete (CRUD) inventory items
- ✅ RESTful API architecture
- ✅ Responsive UI with Tailwind
- ✅ Separation of frontend and backend
- ✅ Ready for deployment

---

## 🖥️ Backend Setup (Flask)

### 1. Navigate to server folder

```bash
cd server
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the server

```bash
python run.py
```

Or using Gunicorn (production):

```bash
gunicorn run:app
```

---

## 🌐 Frontend Setup (React)

### 1. Navigate to client folder

```bash
cd client
```

### 2. Install dependencies

```bash
npm install
```

### 3. Start development server

```bash
npm run dev
```

---

## 🔗 API Integration

The frontend communicates with the backend using **Fetch API**.

Example:

```javascript
fetch("/api/items")
  .then((res) => res.json())
  .then((data) => console.log(data));
```

---

## 📦 Deployment

### Backend (Render)

Uses Procfile:

```
web: gunicorn run:app
```

### Frontend

Build React app:

```bash
npm run build
```

---

## Remote Link

## https://inventory-rho-dun.vercel.app/

## 🤝 Contributing

Contributions are welcome!

1. Fork the repo
2. Create a new branch
3. Commit your changes
4. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**TEAM 6**

---

## ⭐ Notes

This project demonstrates:

- Clean separation of concerns
- REST API design
- React state management with real backend data
