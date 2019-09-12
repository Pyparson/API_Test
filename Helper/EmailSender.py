import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime


class EmailSender:
    # 发送邮件
    @classmethod
    def send_report(self, data, result_file_abs_path):
        # print("Sending report...")
        result_file_name = result_file_abs_path.split("\\")[-1]
        conf = data["emailServer"]
        sender = conf["sender"]
        receivers = conf["receivers"]
        subject = conf["subject"]
        smtp_server = conf["smtp_server"]
        username = conf["username"]
        password = conf["password"]
        msg_root = MIMEMultipart('related')
        msg_root['Subject'] = subject + str(datetime.now()).split('.')[0]
        msg_root["From"] = sender
        msg_root["To"] = ", ".join(receivers)
        with open(result_file_abs_path, "rb") as f:
            content = f.read()
        msg_content_html = MIMEText(content, 'html', 'utf-8')
        msg_attach = MIMEText(content, 'base64', 'utf-8')
        msg_attach["Content-Type"] = 'application/octet-stream'
        msg_attach["Content-Disposition"] = 'attachment; filename=%s' % result_file_name
        msg_root.attach(msg_content_html)
        msg_root.attach(msg_attach)
        smtp = smtplib.SMTP()    
        smtp.connect(smtp_server)
        smtp.login(username, password)    
        smtp.sendmail(sender, receivers, msg_root.as_string())
        smtp.quit()
        # print("Email report has been sent.")

