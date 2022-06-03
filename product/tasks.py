
from celery.schedules import crontab
from celery import shared_task
from models import Link, get_data
import time

@shared_task(run_every=(crontab(minute='*/15')), name="track_for_discount", ignore_result=True)
def track_for_discount():
    items = Link.objects.all()  #take a list of existed items
    for item in items:
        data = get_data(item.url)
        if data[1] < item.current_price:
            item_discount = Link.objects.get(id=item.id)  #take particular object
            item_discount.old_price = item_discount.current_price
            item_discount.current_price = data[1]
            item_discount.save(update_fields=['current_price, old_price'])

                
            """if self.monitored = True: 
                    end_email()"""
            
            
        
@shared_task
def track_for_not_discount():
    items = Link.objects.all()
    for item in items:
        data = get_data(item.url)
        if data[1] > item.old_price:
            item_discount_finished = Link.objects.get(id=item.id)
            item_discount_finished.old_price = item_discount_finished.current_price
            item_discount_finished.current_price = data[1]
            item_discount_finished.save()

while True:
    track_for_discount()
    time.sleep(40)
    #track_for_not_discount()
    #time.sleep(40) 

        