from django.shortcuts import render, redirect
from django.http import HttpResponse
from .contactform import ContactForm
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings


emailuser = settings.EMAIL_HOST_USER


def ContactView(request):
    if request.method == "GET":
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Recebemos a sua mensagem. Entraremos em contacto assim que possível!')
            form.save()
            subject = f'{request.POST.get("nome_completo")}-{request.POST.get("email")}'
            from_email = emailuser
            mensagem = f' O utilizador {request.POST.get("nome_completo")} enviou a seguinte mensagem: \n {request.POST.get("mensagem")}, \n entre em contacto através do e-mail: \n {request.POST.get("email")}'
            try:
                send_mail(subject, mensagem, from_email, [emailuser])
            except BadHeaderError:
                return HttpResponse('BadHeaderError')
            return redirect('contact')

    context = {
	    'form': form,
    }

    return render(request, 'contact/contact.html', context)


