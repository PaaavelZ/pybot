import threading
import time
from datetime import date

from config import SECONDS_IN_DAY
from db import Database


def remove_overdue_hws():
    while True:
        with Database() as db:
            hws = db.get_hws()

            for subj in hws.keys():
                hws_by_subj = hws[subj]
                for hw in hws_by_subj:
                    hw_deadline_str = hw[1]
                    hw_deadline = date(int(hw_deadline_str[0:4]), int(hw_deadline_str[5:7]), int(hw_deadline_str[8:10]))
                    if (date.today() - hw_deadline).days >= 1:
                        hw_id = db.get_hw_id(hw_deadline)
                        db.delete_hw(hw_id)

        time.sleep(SECONDS_IN_DAY)


def start():
    overdue_hw_remover = threading.Thread(target=remove_overdue_hws, name="overdue_hw_remover", daemon=True)
    overdue_hw_remover.start()
