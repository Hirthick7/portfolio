# Hirthick M - Professional Portfolio Website

A full-stack professional portfolio website showcasing my skills, projects, and experience as a Software Engineer and Engineering Student.

## 🌟 Features

- **Royal Theme Design**: Classic and professional design with deep navy blue, royal gold accents, and elegant typography
- **3D Animations**: Rotating 3D gear in hero section, floating geometric shapes, and interactive card effects
- **Multi-Page Structure**: Separate pages for Home, About, Projects, Skills, and Contact
- **Dark Mode**: Toggle between light and dark themes with persistent preference storage
- **Responsive Design**: Fully responsive across desktop, tablet, and mobile devices
- **Contact Form**: Integrated contact form with MongoDB storage and email validation
- **Email Notifications**: Automatic email notifications sent to your inbox when someone submits the contact form
- **Smooth Animations**: Parallax scrolling, fade-in effects, and animated skill bars
- **Interactive Elements**: 3D tilt effects, hover animations, and scroll progress indicator

## 🛠️ Technology Stack

### Frontend
- HTML5
- CSS3 (with custom properties and animations)
- Vanilla JavaScript
- Google Fonts (Playfair Display, Inter)
- Font Awesome Icons

### Backend
- Python 3.x
- Flask 3.0.0
- Flask-Mail 0.9.1
- PyMongo 4.6.1
- Python-dotenv 1.0.0

### Database
- MongoDB (local or MongoDB Atlas)

## 📁 Project Structure

```
portfolio/
├── app.py                 # Flask application with routes
├── models.py             # MongoDB models and database connection
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
├── README.md            # This file
├── templates/           # HTML templates
│   ├── base.html       # Base template with navigation
│   ├── index.html      # Home page
│   ├── about.html      # About page
│   ├── projects.html   # Projects page
│   ├── skills.html     # Skills page
│   └── contact.html    # Contact page
└── static/
    ├── css/
    │   └── style.css   # Main stylesheet
    ├── js/
    │   └── main.js     # JavaScript functionality
    └── images/         # Image assets
```

## 🚀 Setup Instructions

### Prerequisites

- Python 3.8 or higher
- MongoDB (local installation) OR MongoDB Atlas account
- pip (Python package manager)

### Installation

1. **Clone or navigate to the project directory**
   ```bash
   cd "c:\Users\mhirt\OneDrive\Documents\vs code\portfolio"
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure environment variables**
   - Copy `.env.example` to `.env`
   - Update the MongoDB connection string if needed:
     ```
     # For local MongoDB
     MONGO_URI=mongodb://localhost:27017/
     
     # For MongoDB Atlas
     MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/
     ```
   - Configure email settings (see Email Configuration section below)

6. **Ensure MongoDB is running**
   - For local MongoDB: Start the MongoDB service
   - For MongoDB Atlas: Ensure your cluster is active and connection string is correct

## 📧 Email Configuration

The contact form sends email notifications when visitors submit messages. To enable this feature:

### Gmail Setup (Recommended)

1. **Enable 2-Factor Authentication** on your Gmail account
2. **Generate App Password**:
   - Go to [Google Account Security](https://myaccount.google.com/security)
   - Navigate to "2-Step Verification" → "App passwords"
   - Create a new app password for "Mail"
   - Copy the 16-character password

3. **Update `.env` file**:
   ```
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-app-password-here
   RECIPIENT_EMAIL=mhirthick07@gmail.com
   ```

### Email Features

When someone submits the contact form:
- ✅ You receive a beautifully formatted HTML email
- ✅ Email includes sender's name, email, message, and timestamp
- ✅ Reply-to is set to the visitor's email (you can reply directly)
- ✅ Message is also saved to MongoDB as backup
- ✅ User receives confirmation message on the website

### Running the Application

1. **Start the Flask development server**
   ```bash
   python app.py
   ```

2. **Open your browser and navigate to**
   ```
   http://localhost:5000
   ```

## 📝 MongoDB Setup

### Option 1: Local MongoDB

1. Install MongoDB Community Edition from [mongodb.com](https://www.mongodb.com/try/download/community)
2. Start MongoDB service:
   - Windows: MongoDB should start automatically as a service
   - macOS: `brew services start mongodb-community`
   - Linux: `sudo systemctl start mongod`

### Option 2: MongoDB Atlas (Cloud)

1. Create a free account at [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
2. Create a new cluster
3. Get your connection string from the "Connect" button
4. Update `.env` file with your Atlas connection string
5. Whitelist your IP address in Atlas Network Access

## 🎨 Features Overview

### Home Page
- Hero section with 3D rotating gear animation
- Quick about summary
- Skills preview with icons
- Featured MedClinic AI project
- Call-to-action sections

### About Page
- Detailed personal introduction
- Engineering background
- Career vision
- Animated timeline of education journey
- Personal interests section

### Projects Page
- Comprehensive MedClinic AI project showcase
- Problem statement and solution
- Key features and tech stack
- Demo and GitHub links

### Skills Page
- Categorized technical skills with animated progress bars
- Soft skills with detailed descriptions
- Interactive 3D tilt effects on skill cards

### Contact Page
- Contact form with validation
- Email, LinkedIn, and GitHub links
- Flash messages for form submission feedback
- MongoDB storage for messages

## 🎯 Key Features Explained

### Dark Mode
- Toggle between light and dark themes
- Preference saved in localStorage
- Smooth transition between themes

### Animations
- Page loading animation
- Scroll progress indicator
- Fade-in animations on scroll
- 3D rotating gear in hero section
- Parallax scrolling effects
- Animated skill progress bars

### Form Validation
- Client-side validation with JavaScript
- Server-side validation with Flask
- Email format validation
- Minimum length requirements
- Real-time feedback

## 🔧 Customization

### Changing Colors
Edit CSS custom properties in `static/css/style.css`:
```css
:root {
    --navy-dark: #0a1128;
    --gold-primary: #d4af37;
    /* ... other colors */
}
```

### Updating Content
- Personal information: Edit HTML templates in `templates/`
- Skills and percentages: Update `templates/skills.html`
- Projects: Update `templates/projects.html`

## 📧 Contact Form Data

Contact form submissions are stored in MongoDB in the `contact_messages` collection with the following structure:
```json
{
    "name": "Sender Name",
    "email": "sender@example.com",
    "message": "Message content",
    "created_at": "2026-02-17T10:30:00Z",
    "read": false
}
```

## 🌐 Deployment

For production deployment:

1. Set `FLASK_DEBUG=False` in `.env`
2. Use a production WSGI server like Gunicorn:
   ```bash
   pip install gunicorn
   gunicorn app:app
   ```
3. Configure environment variables on your hosting platform
4. Ensure MongoDB connection string is secure

## 📄 License

This project is created for personal portfolio purposes.

## 👤 Author

**Hirthick M**
- Email: mhirthick07@gmail.com
- LinkedIn: [linkedin.com/in/hirthick-m](https://www.linkedin.com/in/hirthick-m)
- GitHub: [github.com/hirthick-m](https://github.com/hirthick-m)

---

Built with ❤️ using Flask, MongoDB, and modern web technologies.
