import imaplib
import email
import os
import re
from email.parser import HeaderParser


user = # email address of user
password = # password
imap_url = # imap server address
downloads = os.getcwd()
attachment_dir = downloads+'/downloads/'

authorized_senders = [
"""    enter email addresses here 
   separated by comma, to authorize them """
]


# Connect to an IMAP server
def connect(server, user, password):
    m = imaplib.IMAP4_SSL(server)
    m.login(user, password)
    m.select(readonly=False)
    return m

# Download all attachment files for a given email


def downloaAttachmentsInEmail(m, emailid, outputdir):
    resp, data = m.fetch(emailid, '(RFC822)')
    header_data = data[0][1].decode('utf-8')
    parser = HeaderParser()
    msg = parser.parsestr(header_data)
    print(msg.get('from'))
    email_address = re.findall(
        "([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", msg.get('from'))

    # see if sender is authorized
    if email_address[0] in authorized_senders:
        mail = email.message_from_bytes(data[0][1])

        if mail.get_content_maintype() != 'multipart':
            return
        for part in mail.walk():
            if part.get_content_maintype() != 'multipart' and part.get('Content-Disposition') is not None:
                filename = part.get_filename()
                if bool(filename):
                    filePath = outputdir+filename

                    # the block below must be wrapped in if/else loop for various tasks
                    with open(filePath, 'wb') as f:
                        f.write(part.get_payload(decode=True))


# Download all the attachment files for all emails in the inbox.
def downloadAllAttachmentsInInbox(server, user, password, outputdir):
    m = connect(server, user, password)
    resp, items = m.search(None, 'INBOX', '(UNSEEN)')
    items = items[0].split()
    for emailid in items:
        downloaAttachmentsInEmail(m, emailid, outputdir)
        m.store(emailid, '+FLAGS', '\Seen')


downloadAllAttachmentsInInbox(imap_url, user, password, attachment_dir)