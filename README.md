# Study Smart Project

**Free Online Study Planner**

Take control of your learning with Study Smart — an intuitive, web-based platform designed to help you organize, track, and optimize your study sessions. Whether you're a student, a lifelong learner, or preparing for exams, Study Smart empowers you to plan effectively and achieve your academic goals.

---

## 🚀 Features

- **Personalized Study Planning**: Create, manage, and customize your study schedules with ease.
- **User Authentication**: Secure signup and login to keep your plans private.
- **Progress Tracking**: Visualize your achievements and stay motivated.
- **Responsive Design**: Accessible on desktop and mobile devices.
- **Modern UI**: Clean and user-friendly interface for distraction-free planning.

---

## 🛠️ Technologies Used

- **Python** & **Flask**: Backend web framework for robust, scalable development.
- **Flask-Migrate**: Database migrations for seamless schema updates.
- **HTML5** & **CSS3**: Clean, responsive layouts and styles.
- **JavaScript**: Interactive front-end features.
- **Gunicorn**: Production-ready WSGI server.
- **SQLAlchemy**: Powerful ORM for database management.

---

## 📁 Project Structure

```
study_smart_project/
│
├── main.py                # Application entrypoint (Gunicorn-ready)
├── Procfile               # Deployment configuration
├── study_smart/
│   ├── __init__.py        # App factory
│   ├── auth.py            # Authentication logic
│   ├── forms.py           # Web forms
│   ├── models.py          # Database models
│   ├── views.py           # Route handlers and views
│   ├── static/            # CSS, JS, images
│   └── templates/         # HTML templates
│
└── ...                    # Additional configs and files
```

---

## 🏁 Getting Started

1. **Clone the repository**  
   ```bash
   git clone https://github.com/collin-s46/study_smart_project.git
   cd study_smart_project
   ```

2. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**  
   (Configure your database URI and secret keys)

4. **Run database migrations**  
   ```bash
   flask db upgrade
   ```

5. **Start the app locally**  
   ```bash
   flask run
   ```
   Or with Gunicorn:
   ```bash
   gunicorn main:app
   ```

---

## 💡 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests to help improve Study Smart.

---

## 📃 License

This project is open-source and free to use.

---

Unleash your academic potential — start planning smarter, not harder!
