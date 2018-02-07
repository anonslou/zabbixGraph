#!/usr/bin/env python3

from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
import os
from email.mime.base import MIMEBase
from email import encoders
from email.mime.text import MIMEText

class MailMe:

    def __init__(self, addr_from, addr_to):
        self.addr_from = addr_from
        self.addr_to = addr_to
        self.msg = MIMEMultipart()
        self.msg['To'] = self.addr_to
        self.msg['From'] = self.addr_from
    
    def set_subjmes(self, subj=None, mes=None):
        if subj:
            self.msg['Subject'] = subj
        if mes:
            self.msg.attach(MIMEText(mes))

    def add_attach(self, filename):
        basename = os.path.basename(filename)
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(filename, 'rb').read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % basename)
        self.msg.attach(part)

    def send_mail(self, server):
        s = SMTP(server)
        to = self.addr_to.split(',')
        s.sendmail(self.addr_from, to, self.msg.as_string())
        s.quit()

