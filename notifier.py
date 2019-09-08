import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class EmailSender:

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.server = smtplib.SMTP('smtp.gmail.com', 587)
        self.login_server()
    
    def login_server(self):
        self.server.ehlo()
        self.server.starttls()
        self.server.ehlo()
        self.server.login(self.email, self.password)

    def compose_header(self, from_addr, to_addr, subject):
        msg = MIMEMultipart()
        msg['From'] = from_addr
        msg['To'] = to_addr
        msg['Subject'] = subject
        return msg
    
    def attach_body(self, body, msg):
        msg.attach(MIMEText(body, 'plain'))
        
    def send_mail(self, from_addr, to_addr, subject, body):
        msg = self.compose_header(from_addr, to_addr, subject)
        self.attach_body(body, msg)
        text = msg.as_string()
        self.server.sendmail(from_addr, to_addr, text)


if __name__ == "__main__":
    email = 'kzjyzz@gmail.com'
    password = 'kelvin123zhang'
    sender = EmailSender(email, password)
    sender.send_mail(email, 'kelvinzhangjy@hotmail.com', 'hello', 'its me')