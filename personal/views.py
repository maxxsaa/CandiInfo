from django.shortcuts import render, redirect 
from datetime import datetime, date, timedelta
from personal.models import User, Lieu, Reservation
from django.contrib.auth import authenticate, login, logout
import random
import string

# Create your views here.

def home_view(request):
    if 'déconnexion' in request.GET :
        del request.session['email']
        return redirect('/login')
    if request.session['email'] is not None :
        user = User.objects.get(email=request.session['email'])
        username = user.firstname
        template_values = {'name' : username}
        return render(request, 'personal/home.html', template_values)
    else:
        return redirect('/login')

def login_view(request):
    if 'email' in request.GET and 'password' in request.GET :
        enteredEmail = request.GET['email']
        enteredPassword = request.GET['password']
        if len(User.objects.filter(email=enteredEmail).filter(password=enteredPassword)) == 1 :
            request.session['email'] = request.GET['email']
            return redirect('/home')
        else:
            template_values = {'error' : 'Mauvais identifiants'}
            return render(request,'personal/login.html', template_values)        
    else:
        template_values = {}
        return render(request, 'personal/login.html', template_values)


def register_view(request):
    def reverse(s):
        if len(s) == 0:
            return s
        else:
            return reverse(s[1:]) + s[0]
    
    if 'email' in request.GET :
        stri = reverse( request.session['str'])
        if request.GET['CAPTCHA'] == stri :
            newUser = User(firstname= request.GET['firstname'],
                        lastname= request.GET['lastname'],
                        email=request.GET['email'],
                        password=request.GET['password'],
                        gender=request.GET['gender'],
                        gerant=request.GET['gerant']
                        )
            newUser.save()
            return redirect('/login')
        else:
            letters = string.ascii_lowercase
            result_str = ''.join(random.choice(letters) for i in range(5))
            template_values = {'error' : 'Veuillez réessayer.', 'str' : result_str } 
            return render(request, 'personal/register.html', template_values)
    else : 
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(5))
        request.session['str'] = result_str
        
        template_values = {'str' : result_str}
        return render(request, 'personal/register.html', template_values)

def encoder_view(request):
    email = request.session['email']
    current_user = User.objects.get(email=email)
    if current_user.gerant == True :
        if 'supprimer' in request.GET :
            Lieu.objects.filter(id=request.GET['supprimer']).delete()
        if 'name' in request.GET :
            newLieu = Lieu(name= request.GET['name'],
                        capacity= request.GET['capacity'],
                        provirus=request.GET['provirus'],
                        proprietaire= current_user
                        )
            newLieu.save()
            return redirect('/encoder')
        else:
            listetab = Lieu.objects.filter(proprietaire=current_user)
            if listetab is not None :
                liste = listetab
            template_values = {'liste' : liste}
            return render(request,'personal/encoder.html', template_values)
    else:
        template_values = {'pasgerant' : "Vous n'êtes pas gérant et ne pouvez pas encoder d'établissement. Veuillez retourner au menu."}
        return render(request,'personal/encoder.html', template_values)

def reservation_view(request):
    email = request.session['email']
    current_user = User.objects.get(email=email)
    if 'supprimer' in request.GET :
        Reservation.objects.filter(id=request.GET['supprimer']).delete()
    listeres = Reservation.objects.filter(personne=current_user)
    liste1 = Reservation.objects.filter(personne=current_user)
    listedanger = []
    for i in liste1 :
        lieu = i.lieu
        lieu2 = Lieu.objects.get(name=lieu)
        if lieu2.provirus == True :
            listedanger.append(lieu2)
    if listedanger is not None :
        danger = 'Attention : Vous avez fait une réservation dans un lieu enclin à transmettre le virus. Veuillez respecter les règles sanitaires.' 
    if 'lieu' in request.GET :
        endroit = Lieu.objects.get(id=request.GET['lieu'])
        capacite = endroit.capacity
        somme = int(request.GET['number'])
        for i in Reservation.objects.filter(date=request.GET['date']).filter(lieu=endroit):
            somme += i.nombre
        if current_user.positif is not True :    
            if int(somme) <= int(capacite) :
                newRes = Reservation(nombre=request.GET['number'],
                lieu=endroit,
                date=request.GET['date'],
                personne= current_user)
                newRes.save()
                return redirect('/reservations')
            else: 
                error = 'La capacité du lieu est insuffisante.'
                template_values = {'error' : error, 'listeres' : listeres, 'danger' : danger}
                return render(request, 'personal/reserver.html', template_values)
        else :
            error = 'Vous ne pouvez pas faire de réservation car vous êtes infecté.'
            template_values = {'error' : error, 'listeres' : listeres, 'danger' : danger}
            return render(request, 'personal/reserver.html', template_values)
    else:
        if 'Provirus' in request.GET :
            prov = request.GET['Provirus']
            
            listelieu = Lieu.objects.filter(provirus= prov)
            template_values = {'listelieu' : listelieu, 'suite' : 'suite', 'listeres' : listeres, 'danger' : danger}
            return render(request,'personal/reserver.html', template_values)
        else: 
            if listeres is not None :
                liste = listeres
                template_values = {'listeres' : liste, 'danger' : danger}
                return render(request,'personal/reserver.html', template_values)
    


def positif_view(request):
    email = request.session['email']
    user = User.objects.get(email=email)
    danger = []
    user_pos = User.objects.filter(positif=True)
    for i in Reservation.objects.filter(personne=user):
        for j in user_pos :
            for k in Reservation.objects.filter(personne= j) :
                if j.DateTest == k.date and i.lieu == k.lieu :
                    if i not in danger :
                        danger.append(i)
    


    if 'positif' in request.GET :
        date = request.GET['date']
        user.positif = True
        user.DateTest = date
        user.save()
        template_values = {'valide' : 'Merci. Nous nous chargeons du reste.' }
        return render(request, 'personal/positif.html', template_values)
    else :
        if user.positif == True :
            test = user.DateTest
            template_values={'état' : 'Vous êtes positif.ve au coronavirus.' , 'test' : f'{'Vous avez fait votre test le'} {test}'}
            return render(request, 'personal/positif.html', template_values)
        else:
            template_values={'neg' : 'Vous êtes négatif.ve au coronavirus.' , 'test' : "Vous n'avez pas fait de test.", 'contact' : danger}
            return render(request, 'personal/positif.html', template_values)


def stat_view(request):
    connecté = False
    if 'email' in request.session : 
        connecté = True
    
    contactpos = 0
    res = []
    #nouveaux cas positifs 30 derniers jours
    caspos =0
    for i in User.objects.filter(positif=True):
        if (date.today() - i.DateTest ) < timedelta(days=30) :
            caspos += 1
    #nombre de personnes en contact avec les cas positifs 

    # on prend chaque réservation d'un cas positif et on récolte les autres réservations identiques
    #on récolte le nombre de personnes total - le nombre de cas positifs
    user_pos = User.objects.filter(positif=True)
    nombre_contact = 0
    for i in user_pos :
        for j in Reservation.objects.filter(personne=i): #pour chaque réservation d'un cas positif
            for k in Reservation.objects.all():
                us = k.personne
                if k.date == j.date and k.lieu == j.lieu :
                    user = User.objects.get(id=us.id)
                    if user.positif is not True :
                        nombre_contact += k.nombre
    for i in user_pos :
        for j in Reservation.objects.filter(personne=i):
            nombre_contact += (j.nombre - 1)
                    


    
    template_values={'caspos' : caspos, 'contactpos' : nombre_contact, 'connecté' : connecté}
    return render(request, 'personal/stat.html', template_values)