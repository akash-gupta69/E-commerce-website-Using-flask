from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from app.auth import auth
from app.models.user import User
from app import db, bcrypt, mail
from itsdangerous import URLSafeTimedSerializer
from flask import current_app
from flask_mail import Message
import requests


def get_reset_token(email):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return s.dumps(email, salt='password-reset-salt')

def verify_reset_token(token, expiration=1800):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = s.loads(token, salt='password-reset-salt', max_age=expiration)
    except Exception:
        return None
    return email


def verify_recaptcha(recaptcha_response):
    """Verify the reCAPTCHA response token with Google's API."""
    if not recaptcha_response:
        return False
    secret_key = current_app.config.get('RECAPTCHA_SECRET_KEY', '')
    payload = {
        'secret': secret_key,
        'response': recaptcha_response
    }
    try:
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=payload, timeout=5)
        result = r.json()
        return result.get('success', False)
    except Exception:
        return False


# ---------------- REGISTER ----------------

@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        existing_user = User.query.filter(
            (User.email == email) | (User.username == username)
        ).first()

        if existing_user:
            flash("User already exists", "danger")
            return redirect(url_for("auth.register"))

        hashed_pw = bcrypt.generate_password_hash(password).decode("utf-8")

        new_user = User(
            username=username,
            email=email,
            password_hash=hashed_pw
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful. Please login.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")


# ---------------- LOGIN ----------------

@auth.route("/login", methods=["GET", "POST"])
def login():
    site_key = current_app.config.get('RECAPTCHA_SITE_KEY', '')
    if request.method == "POST":
        # Verify reCAPTCHA
        recaptcha_response = request.form.get('g-recaptcha-response')
        if not verify_recaptcha(recaptcha_response):
            flash("Please complete the reCAPTCHA verification.", "danger")
            return redirect(url_for("auth.login"))

        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password_hash, password):
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for("shop.home"))

        flash("Invalid credentials", "danger")

    return render_template("auth/login.html", site_key=site_key)


# ---------------- LOGOUT ----------------

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully", "info")
    return redirect(url_for("auth.login"))


# ---------------- FORGOT PASSWORD ----------------

@auth.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    site_key = current_app.config.get('RECAPTCHA_SITE_KEY', '')
    if request.method == "POST":
        # Verify reCAPTCHA
        recaptcha_response = request.form.get('g-recaptcha-response')
        if not verify_recaptcha(recaptcha_response):
            flash("Please complete the reCAPTCHA verification.", "danger")
            return redirect(url_for("auth.forgot_password"))

        email = request.form.get("email", "").strip()
        user = User.query.filter_by(email=email).first()
        if user:
            token = get_reset_token(email)
            reset_url = url_for("auth.reset_password", token=token, _external=True)
            
            # Try sending email; if MAIL_SUPPRESS_SEND is True it prints to console
            try:
                msg = Message("AuxyysKart - Password Reset",
                              recipients=[email])
                msg.html = f"""
                <h2>Password Reset Request</h2>
                <p>Hi {user.username},</p>
                <p>Click the link below to reset your password:</p>
                <p><a href="{reset_url}">{reset_url}</a></p>
                <p>This link expires in 30 minutes.</p>
                <p>If you didn't request this, ignore this email.</p>
                """
                mail.send(msg)
            except Exception:
                pass
            
            # Always print to console for dev convenience
            print(f"\n{'='*50}")
            print(f"PASSWORD RESET LINK for {email}:")
            print(f"{reset_url}")
            print(f"{'='*50}\n")
        
        # Always show same message for security
        flash("If that email exists, a reset link has been sent. Check your email (or Flask console).", "info")
        return redirect(url_for("auth.login"))
    
    return render_template("auth/forgot_password.html", site_key=site_key)


# ---------------- RESET PASSWORD ----------------

@auth.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    email = verify_reset_token(token)
    if not email:
        flash("The reset link is invalid or has expired.", "danger")
        return redirect(url_for("auth.forgot_password"))
    
    if request.method == "POST":
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")
        
        if not password or len(password) < 4:
            flash("Password must be at least 4 characters.", "danger")
            return render_template("auth/reset_password.html", token=token)
        
        if password != confirm:
            flash("Passwords do not match.", "danger")
            return render_template("auth/reset_password.html", token=token)
        
        user = User.query.filter_by(email=email).first()
        if user:
            user.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")
            db.session.commit()
            flash("Your password has been reset! Please log in.", "success")
            return redirect(url_for("auth.login"))
        
        flash("User not found.", "danger")
        return redirect(url_for("auth.forgot_password"))
    
    return render_template("auth/reset_password.html", token=token)