import logging
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from Util.Excpt import EmailSendError

#第三方邮件服务 qq.com  vowrttntbunydbcg
class EmailSender:
    def __init__(self, server="", port=0, sender="", sender_password="",
            sender_name = None):
        self.server = smtplib.SMTP_SSL(server, port)  #smtp.qq.com 465
        self.sender = sender  #发件人邮箱账号
        self.sender_password = sender_password #发件人密码
        self.sender_name = sender_name #发件人昵称

    def send(self, subject, recvs, content):
        """
        @param recvs It can be a list, such as ['1@163.com', '2@163.com'].
        """
        try:
            msg = MIMEText(content, 'plain', 'utf-8')
            msg['From'] = formataddr([self.sender_name, self.sender])
            msg['Subject'] = subject  #主题
            self.server.login(self.sender, self.sender_password)
            if isinstance(recvs, list):
                for mail in recvs:
                    msg['To'] = formataddr([mail.split('@')[0], mail])
                    self.server.sendmail(self.sender, mail, msg.as_string())
            else:
                mail = recvs
                msg['To'] = formataddr([mail.split('@')[0], mail])
                self.server.sendmail(self.sender, mail, msg.as_string())
            self.server.quit()
        except Exception as err:
            logging.warning('send exception: {}'.format(err))
            raise EmailSendError()


'''
Emailclient = EmailSender("smtp.qq.com",465,"3308200258@qq.com","vowrttntbunydbcg","purplecity")
Emailclient.send("test","2239646614@qq.com","hello email")
'''
