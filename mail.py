import logging
import smtplib
import time
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Mail:
    fromaddr = ""
    password = ""
    toaddr = ""

    def main(self, attachment: bool, **kwargs):
        msg = MIMEMultipart()
        msg['From'] = self.fromaddr
        msg['To'] = self.toaddr
        send_time = time.strftime("%m/%d/%Y, %H:%M:%S", time.localtime())
        if attachment:
            file_name = kwargs['file_name']
            msg['Subject'] = "Changing rugs price"
            body = f"last changed: {send_time}"
            msg.attach(MIMEText(body, 'plain'))
            attachment = open(file_name, "rb")
            p = MIMEBase('application', 'octet-stream')
            p.set_payload(attachment.read())
            encoders.encode_base64(p)
            p.add_header('Content-Disposition', "attachment; filename= %s" % file_name)
        else:
            msg['Subject'] = "start crawling"
            body = f"Start crawling progress at: {send_time}"
            msg.attach(MIMEText(body, 'plain'))
            p = MIMEBase('application', 'octet-stream')
        msg.attach(p)
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(self.fromaddr, self.password)
        text = msg.as_string()
        logging.warning('sending...')
        s.sendmail(self.fromaddr, self.toaddr, text)
        logging.warning('email sent.')
        s.quit()

    def __init__(self, attachment):
        file_name = 'output1.xlsx'
        self.main(attachment, file_name=file_name)
