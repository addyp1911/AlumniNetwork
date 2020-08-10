from django.core.paginator import EmptyPage
from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import redirect, reverse
import sendgrid
from sendgrid.helpers.mail import *
from alumni_network import settings


def url_validator(value):
    """A custom method to validate any website url """

    import re
    regex = re.compile(
            r'^https?://|www\.|https?://www\.' # http:// or https:// or www.
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|' #domain...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    if value and not regex.match(value):
        raise AssertionError("The website url is invalid")
    return value

def paginate(data, paginator, pagenumber):
    """
    This method to create the paginated results in Search view.
    """

    if int(pagenumber) > paginator.num_pages:
        raise ValidationError("Not enough pages", code=404)
    try:
        previous_page_number = paginator.page(pagenumber).previous_page_number()
    except EmptyPage:
        previous_page_number = None
    try:
        next_page_number = paginator.page(pagenumber).next_page_number()
    except EmptyPage:
        next_page_number = None
    return data


def send_email(subject, body, FROM, recipient, msg_html):
    '''
    This method create the mail and send it to recipient.
    :param recipient: receiver of mail
    :param subject: subject line of the mail
    :param body: body of the mail
    '''
    try:
        sg = sendgrid.SendGridAPIClient(apikey=settings.SENDGRID_API_KEY)
        TO = recipient if type(recipient) is list else [recipient]
        content = Content('text/html', msg_html)
        mail = Mail(FROM, TO, subject, content)
        msg = sg.client.mail.send.post(request_body=mail.get())             
        return msg 
    except Exception:
        return redirect(reverse('forgot-password'))    