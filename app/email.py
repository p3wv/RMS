from threading import Thread
from flask import current_app, render_template, views
from flask_mail import Message
from . import mail
# from .models import Order
# from .auth .views import order

def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object() # type: ignore
    msg = Message(app.config['RMS_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                 sender=app.config['RMS_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    thr.join()
    return thr

def send_order_confirmation_email(to, cart_items):
    app = current_app._get_current_object() #type: ignore
    subject = 'Order Confirmation'
    sender = app.config['RMS_MAIL_SENDER']
    prefix = app.config['RMS_MAIL_SUBJECT_PREFIX']
    recipients = [to]

    items_description = []
    for item in cart_items:
        item_name = item.get('name', '')
        item_quantity = item.get('quantity', 0)
        item_description = f"{item_name} (Quantity: {item_quantity})"
        items_description.append(item_description)

    email_body = "Thank you for your order!\n\nOrdered Items:\n"
    email_body += '\n'.join(items_description)

    msg = Message(prefix + ' ' + subject, sender=sender, recipients=recipients)
    msg.body = email_body

    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)
