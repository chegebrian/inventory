from flask_mailman import EmailMessage
from flask import current_app
import traceback


# =============================================
# INVITE EMAIL
# =============================================


from flask_mailman import EmailMessage

def send_invite_email(to_email, invite_link, role, store_name):
    try:
        html_body = f"""
        <html>
            <body>
                <h2>You're invited 🎉</h2>
                <p>You have been invited to join <b>{store_name}</b> as <b>{role}</b>.</p>

                <p>
                    Click below to register:
                </p>

                <a href="{invite_link}"
                   style="padding:10px 20px;background:#4F46E5;color:white;text-decoration:none;border-radius:6px;">
                   Complete Registration
                </a>

                <p style="font-size:12px;color:gray;">
                    If button doesn't work, copy this link:
                </p>

                <p>{invite_link}</p>
            </body>
        </html>
        """

        msg = EmailMessage(
            subject=f"Invite to join {store_name}",
            body=html_body,
            to=[to_email]
        )

        msg.content_subtype = "html"  # 🔥 IMPORTANT

        msg.send()

        print("✅ Invite email sent")
        return True

    except Exception as e:
        print(f"❌ EMAIL ERROR: {str(e)}")
        return False

# =============================================
# RESET PASSWORD EMAIL
# =============================================
def send_reset_password_email(to_email, reset_link):
    try:
        subject = "Reset Your Password - Local Shop"

        text_body = f"""
Password Reset Request

Click the link below to reset your password:
{reset_link}

This link expires in 2 hours.
"""

        html_body = f"""
<!DOCTYPE html>
<html>
<body style="font-family: Arial; max-width: 600px; margin: auto; padding: 20px;">

    <div style="background: #DC2626; padding: 20px; border-radius: 10px; text-align: center;">
        <h1 style="color: white;">🔐 Password Reset</h1>
    </div>

    <div style="background: #F9FAFB; padding: 20px; margin-top: 20px; border-radius: 10px;">
        <h2>Reset Your Password</h2>

        <p>We received a request to reset your password.</p>

        <div style="text-align: center; margin: 30px 0;">
            <a href="{reset_link}"
               style="background: #DC2626; color: white; padding: 12px 24px;
                      border-radius: 8px; text-decoration: none;">
                Reset Password →
            </a>
        </div>

        <p style="font-size: 12px; color: gray;">
            This link expires in 2 hours.
        </p>
    </div>

</body>
</html>
"""

        msg = EmailMessage(
            subject=subject,
            from_email=current_app.config.get("MAIL_DEFAULT_SENDER"),
            to=[to_email],
            body=text_body
        )

        msg.attach_alternative(html_body, "text/html")
        msg.send()

        print(f"✅ Reset email sent to {to_email}")
        return True

    except Exception:
        print("❌ RESET EMAIL ERROR:")
        traceback.print_exc()
        return False