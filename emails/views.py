from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

@login_required
def send_welcome_email(request):
    if request.method == "POST":

        user_email = request.user.email

        if user_email:
            msg = EmailMultiAlternatives(
                subject="MKO Performance - Welcome 👋",
                body="Welcome to MKO Performance!",
                from_email="MKO Performance <mkoperformance@gmail.com>",
                to=[user_email],
            )

            msg.attach_alternative("""
                <html>
                    <body>
                        <h2>Welcome 👋</h2>
                        <p>Your email system is working correctly.</p>
                        <p>Thank you for using <b>MKO Performance</b>.</p>
                    </body>
                </html>
            """, "text/html")

            msg.send()

    return redirect("home")