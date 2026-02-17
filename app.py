from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message
from config import Config
from models import ContactMessage, Database
import re
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)

# Initialize Flask-Mail
mail = Mail(app)

# Email validation regex
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')


def send_contact_email(name, email, message):
    """
    Send email notification when contact form is submitted
    
    Args:
        name (str): Sender's name
        email (str): Sender's email
        message (str): Message content
        
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        msg = Message(
            subject=f'New Contact Form Submission from {name}',
            sender=app.config['MAIL_DEFAULT_SENDER'],
            recipients=[app.config['RECIPIENT_EMAIL']],
            reply_to=email
        )
        
        # Email body
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
        
        # HTML version (optional, for better formatting)
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
    """Projects page"""
    return render_template('projects.html')


@app.route('/skills')
def skills():
    """Skills page"""
    return render_template('skills.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact page with form handling"""
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        message = request.form.get('message', '').strip()
        
        # Validation
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
        
        # Save to database and send email
        try:
            # Try to save to database
            try:
                ContactMessage.create(name, email, message)
                print(f"✓ Message saved to database successfully")
            except Exception as db_error:
                print(f"✗ Database error: {db_error}")
                import traceback
                traceback.print_exc()
                # Continue even if database fails
            
            # Try to send email
            try:
                email_sent = send_contact_email(name, email, message)
                if email_sent:
                    print(f"✓ Email sent successfully")
                    flash('Thank you for your message! I will get back to you soon.', 'success')
                else:
                    print(f"✗ Email sending failed")
                    flash('Your message has been saved, but there was an issue sending the email notification. I will still receive your message.', 'success')
            except Exception as email_error:
                print(f"✗ Email error: {email_error}")
                import traceback
                traceback.print_exc()
                flash('Your message has been saved, but there was an issue sending the email notification.', 'success')
            
            return redirect(url_for('contact'))
        except Exception as e:
            print(f"✗ General error: {e}")
            import traceback
            traceback.print_exc()
            flash('An error occurred while sending your message. Please try again later.', 'error')
            return render_template('contact.html')
    
    return render_template('contact.html')


@app.teardown_appcontext
def shutdown_session(exception=None):
    """Close database connection when app context ends"""
    Database.close()


if __name__ == '__main__':
    app.run(debug=Config.DEBUG, host='0.0.0.0', port=5000)
