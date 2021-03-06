import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



def send_password_reset_mail(user_email, token):
    server_email = 'sending.from.python@gmail.com'
    server_email_password = 'gmail9393'
    subject = 'Todos Password Reset'

    msg = MIMEMultipart()
    msg['From'] = server_email
    msg['To'] = user_email
    msg['Subject'] = subject
    # TODO: Make this text better
    mail_contents = \
        f'Reset token is http://127.0.0.1:8000/users/password_reset?token={token}'
    msg.attach(MIMEText(mail_contents,'plain'))
    text = msg.as_string()

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(server_email, server_email_password)
    server.sendmail(server_email,user_email, text)
    server.quit()
