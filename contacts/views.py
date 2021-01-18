from django.shortcuts import render, redirect


# Create your views here.
from contacts.models import Contact
from django.core.mail import send_mail
from django.contrib import messages


def contact(request):
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['listing_id']
        realtor_email = request.POST['realtor_email']

        #check if user has made inquiry already
        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contact.objects.all().filter(listing_id=listing_id, user_id=user_id)
            if has_contacted:
                messages.error(request, 'you have already made an inquiry for this listing')
                return redirect('/listings/' + listing_id)

        contact = Contact(listing=listing, listing_id=listing_id, name=name, email=email,
                          phone=phone, messages=message, user_id=user_id)

        contact.save()

        #send email
        send_mail(
            'Property Listing Inquiry',
            'There has been an inquiry for ' + listing,
            'mrumunjanet@gmail.com',
            [realtor_email, 'mrumunjanet@gmail.com'],
            fail_silently=True
        )


        messages.success(request, 'Your request has been submitted, a realtor will get back to you soon')


        return redirect('/listings/'+listing_id )

