import email
import imaplib
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class MailService:

    def __init__(self, login, password, header=''):
        self.GMAIL_SMTP = "smtp.gmail.com"
        self.GMAIL_IMAP = "imap.gmail.com"
        self.login = login
        self.password = password
        self.header = header

    def send_message(self, **kwargs):
        msg = MIMEMultipart()
        msg['From'] = self.login
        msg['To'] = ', '.join(kwargs['recipients'].split(','))
        msg['Subject'] = kwargs['subject']
        msg.attach(MIMEText(kwargs['message']))

        ms = smtplib.SMTP(self.GMAIL_SMTP, 587)

        # identify ourselves to smtp gmail client
        ms.ehlo()
        # secure our email with tls encryption
        ms.starttls()
        # re-identify ourselves as an encrypted connection
        ms.ehlo()

        ms.login(self.login, self.password)
        ms.sendmail(self.login, msg['To'], msg.as_string())

        ms.quit()
        # send end

    def receive_mail(self):
        mail = imaplib.IMAP4_SSL(self.GMAIL_IMAP)
        mail.login(self.login, self.password)
        mail.list()
        mail.select("inbox")
        criterion = f'(HEADER Subject {self.header})' if self.header else 'ALL'
        result, data = mail.uid('search', None, criterion)

        assert data[0], 'There are no letters with current header'
        latest_email_uid = data[0].split()[-1]

        result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
        raw_email = data[0][1]

        email_message = email.message_from_bytes(raw_email)

        mail.logout()
        # end receive
        return email_message


def main():
    """Mail service.
    Use commands:
    * s - send email
    * r - receive emails to Inbox"""
    login = input('Please enter the login of Gmail account: ')
    password = input('Please enter the Gmail  password')
    print(main.__doc__)
    command = input('Please enter command: ')
    mx = MailService(login, password)
    if command == 's':
        subj = input('Please enter subject: ')
        recip = input("Please enter recipients delimiter by comma: ")
        mess = input('Please enter message text: ')
        print(subj, recip, mess)
        mx.send_message(subject=subj, recipients=recip, message=mess, header='')
    elif command == 'r':
        mx.receive_mail()
    else:
        print('Command not recognized, please repeat')
        main()


if __name__ == '__main__':
    main()
