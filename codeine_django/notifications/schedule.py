import schedule
import time

from .models import Notification, NotificationObject
from common.models import BaseUser 

def analytics_notifications():
    print("Analytics notifications")

# Run job on a specific day of the week
schedule.every().monday.do(analytics_notifications)

while True:
    # run_pending
    schedule.run_pending()
    time.sleep(1)
