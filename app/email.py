from threading import Thread
from uu import Error
from flask import current_app, render_template, render_template_string
from flask_mail import Message
from . import mail

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
        item_image = item.get('productImage')
        item_name = item.get('productName')
        item_quantity = item.get('quantity', 0)
        
        item_description = f"<li style='display: flex; align-items: center;'><img src='{item_image}' alt='{item_name}' style='height: auto; max-width: 100px; margin-right: 10px;' /><span>{item_name} (x {item_quantity})</span></li>"
        items_description.append(item_description)

    if items_description:
        email_body = "Thank you for your order!<br><br>Ordered Items:<br>"
        email_body += "<ul>"
        email_body += ''.join(items_description)
        email_body += "</ul>"

        msg = Message(prefix + ' ' + subject, sender=sender, recipients=recipients)
        msg.html = render_template_string(email_body)

        thr = Thread(target=send_async_email, args=[app, msg])
        thr.start()
    else:
        raise ValueError("No items in cart")
    
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)
