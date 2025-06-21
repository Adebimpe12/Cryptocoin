from django.shortcuts import render
from django.db import transaction
from django.contrib.auth.models import User
from userApp.models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponsePermanentRedirect
from django.urls import reverse
from rave_python import Rave, RaveExceptions, Misc
from django.core.mail import send_mail
from .forms import Payment_form

# Create your views here.


@login_required
def paymentSuccess(request, user_id):
    user = User.objects.get(id=user_id)
    # send mail to the staff
    send_mail(
        'Payment successful',# Subject of the mail
        'Your subscription to be an artiste on musicapp was successful.', # From email (Sender)
        [user.email], # To email (Receiver)
        fail_silently=False, # Handle any error
    )

    messages.success(request, ('Your payment was successful!')) 
    return HttpResponsePermanentRedirect(reverse('become_artiste', args=(user_id,)))


@login_required
def paymentFail(request, user_id):
    messages.error(request, ('Transaction fails!'))
    return HttpResponsePermanentRedirect(reverse('make_payment', args=(user_id,)))

    
@login_required
def payNow(request, user_id):
    if request.method == "POST":
        user = User.objects.get(id=user_id)
        payment_form = Payment_form(request.POST or None)
        if payment_form.is_valid():
            card_num = payment_form.cleaned_data["card_number"]
            cvv = payment_form.cleaned_data["cvv"]
            exp_date = payment_form.cleaned_data["expire_date"]
            
            # connect to flutter wave for charges
            rave = Rave("FLWPUBK_TEST-public key here", "FLWSECK_TEST-secrete key here", usingEnv = False)

            # Payload with pin
            payload = {
            "cardno": str(card_num),
            "cvv":str(cvv),
            "expirymonth":str(exp_date).split("/")[0],
            "expiryyear": str(exp_date).split("/")[1],
            "amount": 1000000,
            "email": user.email,
            "phonenumber": user.profile.phone,
            "firstname": user.first_name,
            "lastname": user.last_name,
            "IP": "355426087298442",
            }

            try:
                res = rave.Card.charge(payload)

                if res["suggestedAuth"]:
                    arg = Misc.getTypeOfArgsRequired(res["suggestedAuth"])

                    if arg == "pin":
                        Misc.updatePayload(res["suggestedAuth"], payload, pin="3310")
                    
                    res = rave.Card.charge(payload)

                if res["validationRequired"]:
                    rave.Card.validate(res["flwRef"], "")

                res = rave.Card.verify(res["txRef"])
                messages.error(request, ('Payment successful.'))
                return HttpResponsePermanentRedirect(reverse('payment_success', args=(user_id,)))

            except RaveExceptions.CardChargeError as e:
                messages.error(request, ('Charge fails.'))
                return HttpResponsePermanentRedirect(reverse('payment_fails', args=(user_id,)))
            except RaveExceptions.TransactionValidationError as e:
                messages.error(request, ('Transaction fails'))
                return HttpResponsePermanentRedirect(reverse('payment_fails', args=(user_id,)))
            except RaveExceptions.TransactionVerificationError as e:
                messages.error(request, ('Validation fails.'))
                return HttpResponsePermanentRedirect(reverse('payment_fails', args=(user_id,)))
        else:
            messages.error(request, ('Some field in your form are not filled correctly.'))
            return HttpResponsePermanentRedirect(reverse('pay_now', args=(user_id,)))
    else:
        payment_form = Payment_form()
        return render(request, 'paymentApp/payment_form.html', {
        'payment_form':payment_form,
    })
        
