import smtplib
import ssl
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Mail:
    """
    send mail module inspired by: https://realpython.com/python-send-email/
    """

    def __init__(self, settings):
        self.server = settings["server"]
        self.port = settings.get("port", 587)
        self.sender = settings["sender"]
        self.password = settings["password"]

    def connect(self):
        """
        returns a connection to the mail server

        Use the following to send the mail:

        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )

        once the connection is complete
        remember to server.quit()
        """
        context = ssl.create_default_context()
        # Try to log in to server and send email
        server = smtplib.SMTP(self.server, self.port)
        server.ehlo()  # Can be omitted
        server.starttls(context=context)  # Secure the connection
        server.ehlo()  # Can be omitted
        server.login(self.sender, self.password)

        return server

    def sendMail(self, subject, msg, to, mode="html", cc=None, bcc=None, attachments=[]):
        """
        msg: (str)
            is some string containing the message
        to: (str or list)
            is some string containing the message
        mode: (str)
            html | plain
            Use this to select either html or plain text mode
        The rest of the parameters should be evident
        """
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = self.sender
        message["To"] = to if isinstance(to, str) else ", ".join(to)

        mimeMessage = MIMEText(msg, mode)
        message.attach(mimeMessage)

        if cc:
            message["Cc"] = cc if isinstance(cc, str) else ", ".join(cc)
        if bcc:
            message["Bcc"] = bcc if isinstance(bcc, str) else ", ".join(bcc)

        for attachment in attachments:
            with open(attachment, "rb") as handle:
                # Add file as application/octet-stream
                # Email client can usually download this automatically as attachment
                part = MIMEBase("application", "octet-stream")
                part.set_payload(handle.read())

            filename = os.path.basename(attachment)
            # Encode file in ASCII characters to send by email
            encoders.encode_base64(part)

            # Add header as key/value pair to attachment part
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {filename}",
            )
            message.attach(part)

        server = self.connect()
        server.sendmail(
            self.sender, to, message.as_string()
        )
        server.close()
