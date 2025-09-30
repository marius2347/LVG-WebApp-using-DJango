# LVG WebApp (Django)

A web application built using Django.  
This repository contains the full source code, a demo video, and instructions for setup, usage, and contact.

---

## 💾 Repository Contents

```
.
├── lvg_webapp/                   # Django project folder
├── webvideo.mp4                  # Demo video showing the app in action
├── .gitattributes
└── README.md                      # (this file)
```

- The **lvg_webapp/** folder contains all the Django application code (settings, apps, templates, static files, etc.).
- **webvideo.mp4** is a short video recording demonstrating core features of the web app (used as proof of functionality).
- **.gitattributes** is included for consistency in repository behavior.

---

## 🎬 Demo 

You can see the web application in action:

![Demo of LVG WebApp](webvideo.gif)
---

## 🛠️ Setup & Installation

Follow the steps below to run the application locally:

### Prerequisites

- Python 3.x  
- pip (Python package manager)  
- Virtual environment tool (optional but recommended)  
- (Optional) A database like SQLite (default) or PostgreSQL, etc.

### Installation Steps

1. **Clone the repository**  
   ```bash
   git clone https://github.com/marius2347/LVG-WebApp-using-DJango.git
   cd LVG-WebApp-using-DJango
   ```

2. **Create & activate a virtual environment**  
   ```bash
   python3 -m venv venv
   source venv/bin/activate       # On Linux / macOS
   venv\Scripts\activate          # On Windows
   ```

3. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations**  
   ```bash
   python manage.py migrate
   ```

5. **Run the development server**  
   ```bash
   python manage.py runserver
   ```

6. **Access the app in browser**  
   Open [http://127.0.0.1:8000](http://127.0.0.1:8000) or the URL shown in console.

---

## ✅ Features & Functionality

While the full list of features depends on the internal code, typical features you’d expect:

- User authentication (login, logout, registration)  
- CRUD operations (Create / Read / Update / Delete) for domain entities  
- Templates with dynamic rendering  
- Static files (CSS, JavaScript, images)  
- Possibly APIs or AJAX behavior  
- Demo video to showcase actual working features

---

## 🚧 Known Limitations & Future Improvements

- Error handling and validation may need enhancement  
- Unit tests or integration tests might be missing  
- Better UI/UX polish and responsiveness  
- Deployment setup (e.g. using Gunicorn + Nginx)  
- Switch to PostgreSQL or another robust DB in production

---

## 📞 Contact

If you have questions, suggestions, or want to collaborate:

**Email**: mariusc0023@gmail.com


Thank you for checking out **LVG WebApp** — enjoy exploring the code and video demonstration!

