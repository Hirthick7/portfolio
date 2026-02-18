from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mail import Mail, Message
from functools import wraps
from config import Config
from models import ContactMessage, Database, Skill, Certificate, Project
import re
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)

# Initialize Flask-Mail
mail = Mail(app)

# Email validation regex
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')


# ---------------------------------------------------------------------------
# Admin auth helper
# ---------------------------------------------------------------------------

def admin_required(f):
    """Decorator: redirect to admin login if not authenticated."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('admin_logged_in'):
            flash('Please log in to access the admin panel.', 'error')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated


# ---------------------------------------------------------------------------
# Email helper
# ---------------------------------------------------------------------------

def send_contact_email(name, email, message):
    """
    Send email notification when contact form is submitted.
    Returns True if sent successfully, False otherwise.
    """
    try:
        msg = Message(
            subject=f'New Contact Form Submission from {name}',
            sender=app.config['MAIL_DEFAULT_SENDER'],
            recipients=[app.config['RECIPIENT_EMAIL']],
            reply_to=email
        )
        msg.body = f"""
You have received a new message from your portfolio contact form.

From: {name}
Email: {email}
Submitted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Message:
{message}

---
You can reply directly to this email to respond to {name}.
        """
        msg.html = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f4f4f4;">
                    <div style="background-color: #0a1128; color: #d4af37; padding: 20px; text-align: center;">
                        <h2 style="margin: 0;">New Contact Form Submission</h2>
                    </div>
                    <div style="background-color: white; padding: 30px; margin-top: 20px; border-radius: 5px;">
                        <p style="font-size: 16px; margin-bottom: 20px;">
                            You have received a new message from your portfolio website.
                        </p>
                        <table style="width: 100%; border-collapse: collapse;">
                            <tr>
                                <td style="padding: 10px; background-color: #f8f9fa; font-weight: bold; width: 100px;">From:</td>
                                <td style="padding: 10px;">{name}</td>
                            </tr>
                            <tr>
                                <td style="padding: 10px; background-color: #f8f9fa; font-weight: bold;">Email:</td>
                                <td style="padding: 10px;"><a href="mailto:{email}" style="color: #d4af37;">{email}</a></td>
                            </tr>
                            <tr>
                                <td style="padding: 10px; background-color: #f8f9fa; font-weight: bold;">Date:</td>
                                <td style="padding: 10px;">{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</td>
                            </tr>
                        </table>
                        <div style="margin-top: 30px; padding: 20px; background-color: #f8f9fa; border-left: 4px solid #d4af37;">
                            <h3 style="margin-top: 0; color: #0a1128;">Message:</h3>
                            <p style="white-space: pre-wrap;">{message}</p>
                        </div>
                        <p style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; color: #666; font-size: 14px;">
                            You can reply directly to this email to respond to {name}.
                        </p>
                    </div>
                </div>
            </body>
        </html>
        """
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


# ---------------------------------------------------------------------------
# Public routes
# ---------------------------------------------------------------------------

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')


@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')


@app.route('/projects')
def projects():
    """Projects page — passes dynamic projects from DB"""
    try:
        dynamic_projects = Project.get_all()
    except Exception:
        dynamic_projects = []
    return render_template('projects.html', dynamic_projects=dynamic_projects)


@app.route('/skills')
def skills():
    """Skills page — passes dynamic extra skills from DB"""
    try:
        extra_skills = Skill.get_all()
    except Exception:
        extra_skills = []
    return render_template('skills.html', extra_skills=extra_skills)


@app.route('/certificates')
def certificates():
    """Public certificates page"""
    try:
        certs = Certificate.get_all()
    except Exception:
        certs = []
    return render_template('certificates.html', certificates=certs)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact page with form handling"""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        message = request.form.get('message', '').strip()

        errors = []
        if not name or len(name) < 2:
            errors.append('Name must be at least 2 characters long')
        if not email or not EMAIL_REGEX.match(email):
            errors.append('Please enter a valid email address')
        if not message or len(message) < 10:
            errors.append('Message must be at least 10 characters long')

        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('contact.html')

        try:
            try:
                ContactMessage.create(name, email, message)
                print("✓ Message saved to database successfully")
            except Exception as db_error:
                print(f"✗ Database error: {db_error}")

            try:
                email_sent = send_contact_email(name, email, message)
                if email_sent:
                    flash('Thank you for your message! I will get back to you soon.', 'success')
                else:
                    flash('Your message has been saved, but there was an issue sending the email notification.', 'success')
            except Exception as email_error:
                print(f"✗ Email error: {email_error}")
                flash('Your message has been saved, but there was an issue sending the email notification.', 'success')

            return redirect(url_for('contact'))
        except Exception as e:
            print(f"✗ General error: {e}")
            flash('An error occurred while sending your message. Please try again later.', 'error')
            return render_template('contact.html')

    return render_template('contact.html')


# ---------------------------------------------------------------------------
# Admin routes
# ---------------------------------------------------------------------------

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login page"""
    if session.get('admin_logged_in'):
        return redirect(url_for('admin_dashboard'))

    if request.method == 'POST':
        password = request.form.get('password', '')
        if password == app.config['ADMIN_PASSWORD']:
            session['admin_logged_in'] = True
            flash('Welcome back, Hirthick!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Incorrect password. Please try again.', 'error')

    return render_template('admin_login.html')


@app.route('/admin/logout')
def admin_logout():
    """Admin logout"""
    session.pop('admin_logged_in', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('admin_login'))


@app.route('/admin')
@admin_required
def admin_dashboard():
    """Admin dashboard"""
    try:
        skills_list = Skill.get_all()
    except Exception:
        skills_list = []

    try:
        certs_list = Certificate.get_all()
    except Exception:
        certs_list = []

    try:
        messages_list = ContactMessage.get_all()
    except Exception:
        messages_list = []

    try:
        projects_list = Project.get_all()
    except Exception:
        projects_list = []

    return render_template(
        'admin_dashboard.html',
        skills=skills_list,
        certificates=certs_list,
        messages=messages_list,
        projects=projects_list
    )


@app.route('/admin/skills/add', methods=['POST'])
@admin_required
def admin_add_skill():
    """Add a new skill"""
    name = request.form.get('name', '').strip()
    category = request.form.get('category', '').strip()
    proficiency = request.form.get('proficiency', '0').strip()

    if not name or not category:
        flash('Skill name and category are required.', 'error')
        return redirect(url_for('admin_dashboard') + '#skills')

    try:
        proficiency = max(0, min(100, int(proficiency)))
    except ValueError:
        proficiency = 0

    try:
        Skill.create(name, category, proficiency)
        flash(f'Skill "{name}" added successfully!', 'success')
    except Exception as e:
        flash(f'Error adding skill: {e}', 'error')

    return redirect(url_for('admin_dashboard') + '#skills')


@app.route('/admin/skills/delete/<skill_id>', methods=['POST'])
@admin_required
def admin_delete_skill(skill_id):
    """Delete a skill"""
    try:
        Skill.delete(skill_id)
        flash('Skill deleted successfully.', 'success')
    except Exception as e:
        flash(f'Error deleting skill: {e}', 'error')
    return redirect(url_for('admin_dashboard') + '#skills')


@app.route('/admin/certificates/add', methods=['POST'])
@admin_required
def admin_add_certificate():
    """Add a new certificate"""
    title = request.form.get('title', '').strip()
    issuer = request.form.get('issuer', '').strip()
    issue_date = request.form.get('issue_date', '').strip()
    credential_url = request.form.get('credential_url', '').strip()
    description = request.form.get('description', '').strip()

    if not title or not issuer:
        flash('Certificate title and issuer are required.', 'error')
        return redirect(url_for('admin_dashboard') + '#certificates')

    try:
        Certificate.create(title, issuer, issue_date, credential_url, description)
        flash(f'Certificate "{title}" added successfully!', 'success')
    except Exception as e:
        flash(f'Error adding certificate: {e}', 'error')

    return redirect(url_for('admin_dashboard') + '#certificates')


@app.route('/admin/certificates/delete/<cert_id>', methods=['POST'])
@admin_required
def admin_delete_certificate(cert_id):
    """Delete a certificate"""
    try:
        Certificate.delete(cert_id)
        flash('Certificate deleted successfully.', 'success')
    except Exception as e:
        flash(f'Error deleting certificate: {e}', 'error')
    return redirect(url_for('admin_dashboard') + '#certificates')


# ---------------------------------------------------------------------------
# Project admin routes
# ---------------------------------------------------------------------------

@app.route('/admin/projects/add', methods=['POST'])
@admin_required
def admin_add_project():
    """Add a new project"""
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    tags = request.form.get('tags', '').strip()
    github_url = request.form.get('github_url', '').strip()
    live_url = request.form.get('live_url', '').strip()
    icon = request.form.get('icon', '').strip()

    if not title or not description:
        flash('Project title and description are required.', 'error')
        return redirect(url_for('admin_dashboard') + '#projects')

    try:
        Project.create(title, description, tags, github_url, live_url, icon)
        flash(f'Project "{title}" added successfully!', 'success')
    except Exception as e:
        flash(f'Error adding project: {e}', 'error')

    return redirect(url_for('admin_dashboard') + '#projects')


@app.route('/admin/projects/delete/<project_id>', methods=['POST'])
@admin_required
def admin_delete_project(project_id):
    """Delete a project"""
    try:
        Project.delete(project_id)
        flash('Project deleted successfully.', 'success')
    except Exception as e:
        flash(f'Error deleting project: {e}', 'error')
    return redirect(url_for('admin_dashboard') + '#projects')


# ---------------------------------------------------------------------------
# Teardown
# ---------------------------------------------------------------------------

@app.teardown_appcontext
def shutdown_session(exception=None):
    """Close database connection when app context ends"""
    Database.close()


if __name__ == '__main__':
    app.run(debug=Config.DEBUG, host='0.0.0.0', port=5000)
