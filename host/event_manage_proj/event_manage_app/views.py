import uuid
from datetime import datetime, timedelta, date, time
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import *
from django.utils import timezone
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
import random
# Create your views here.

def index(re):
    return render(re,'index.html')

def home(re):
    return render(re,'home.html')

def about(re):
    return render(re,'about.html')

def contact(re):
    return render(re,'contact.html')

def services(re):
    return render(re,'services.html')

def login(re):
    return render(re,'login.html')

def signup(re):
    return render(re,'signup.html')

def usersignup(re):
    if re.method=="POST":
        name = re.POST.get('name')
        email = re.POST.get('email')
        phone_number = re.POST.get('phone_number')
        address = re.POST.get('address')
        district = re.POST.get('district')
        pincode = re.POST.get('pincode')
        date_of_birth = re.POST.get('date_of_birth')
        age = re.POST.get('age')
        username = re.POST.get('username')
        password = re.POST.get('password')
        try:
            existing_email = User.objects.filter(email=email).exists()
            existing_username = User.objects.filter(username=username).exists()
            existing_phone_number = User.objects.filter(phone_number=phone_number).exists()
            if existing_email:
                messages.warning(re,"Mail already registered")
            elif existing_username:
                messages.warning(re,"Username already exists")
            elif existing_phone_number:
                messages.warning(re,"Phonenumber already exists")
            else:
                obj = User.objects.create(name=name, email=email, phone_number=phone_number, address=address, district=district, pincode=pincode, date_of_birth=date_of_birth, age=age, username=username, password=password, )
                obj.save()
                messages.success(re,'Registration Successfull')
        except Exception:
            messages.warning(re, "Data error")
            return render(re, 'usersignup.html')
    return render(re,'usersignup.html')

def organizersignup(re):
    if re.method == "POST":
        name = re.POST.get('name')
        email = re.POST.get('email')
        phone_number = re.POST.get('phone_number')
        address = re.POST.get('address')
        licenseid=re.POST.get('licenseid')
        username = re.POST.get('username')
        password = re.POST.get('password')
        try:
            existing_email = Organizer.objects.filter(email=email).exists()
            existing_username = Organizer.objects.filter(username=username).exists()
            existing_phone_number = Organizer.objects.filter(phone_number=phone_number).exists()
            if existing_email:
                messages.warning(re,"Mail already registered")
            elif existing_username:
                messages.warning(re,"Username already exists")
            elif existing_phone_number:
                messages.warning(re,"Phonenumber already exists")
            else:
                obj = Organizer.objects.create(name=name, email=email, phone_number=phone_number, address=address,licenseid=licenseid, username=username, password=password, )
                obj.save()
                messages.warning(re,'Registration Successfull')
        except Exception:
            messages.warning(re, "Data error")
            return render(re, 'organizersignup.html')
    return render(re, 'organizersignup.html')


def organizerlogin(re):
    if re.method == 'POST':
        username = re.POST.get('username')
        password = re.POST.get('password')
        try:
            datas = Organizer.objects.get(username=username)
            if (datas.password == password):
                re.session['user'] = username
                return redirect(organizerhome)
            else:
                messages.warning(re,"Password mismatch")
        except Exception:
            if username == 'admin' and password == 'admin':
                re.session['admin'] = username
                return redirect(adminhome)
            messages.warning(re,"Username doesn't exists")
            return render(re, 'organizerlogin.html')
    return render(re, 'organizerlogin.html')

def adminlogin(re):
    if re.method == 'POST':
        username = re.POST.get('username')
        password = re.POST.get('password')
        if username == 'admin' and password == 'admin':
            re.session['admin'] = username
            return redirect(adminhome)
        else:
            messages.warning(re, "Password mismatch")
    return render(re,'adminlogin.html')

def userlogin(re):
    if re.method == 'POST':
        username = re.POST.get('username')
        password = re.POST.get('password')
        try:
            datas = User.objects.get(username=username)
            if(datas.password == password):
                re.session['user'] = username
                return redirect(userhome)
            else:
                messages.warning(re,"Password mismatch")
        except Exception:
            if username == 'admin' and password == 'admin':
                re.session['admin'] = username
                return redirect(adminhome)
            messages.warning(re,"Error Occurred")
            # return render(re, 'userlogin.html')
    return render(re, 'userlogin.html')

def userhome(re):
    if 'user' in re.session:
        try:
            c = User.objects.get(username=re.session['user'])
        except:
            messages.warning(re,"Can't access user")
            return redirect(login)
        return render(re, 'userhome.html', {'user': c})
    messages.warning(re,"User not logged in ")
    return redirect(login)

def organizerhome(re):
    if 'user' in re.session:
        c = Organizer.objects.get(username=re.session['user'])
        return render(re,'organizerhome.html',{'user': c})
    messages.warning(re,"Organizer not logged in ")
    return redirect(login)

def adminhome(re):
    if 'admin' in re.session:
        return render(re, 'adminhome.html')
    else:
        messages.warning(re, "Admin not logged in ")
        return redirect(login)

def searchevent(re):
    if re.method == 'POST':
        searchby = re.POST.get('searchby')
        s = re.POST.get('s')
        events = None  # Default to None, if no events are found
        if searchby == 'name':
            events = Event.objects.filter(name__icontains=s,status='paid')
        elif searchby == 'category':
            try:
                categories = EventCategory.objects.filter(name__icontains=s)
                events=[]
                for category in categories:
                    eventlist = Event.objects.filter(category=category)
                    for event in eventlist:
                        events.append(event)

            except EventCategory.DoesNotExist:
                events = None
        elif searchby == 'venue':
            try:
                venues = Venue.objects.filter(name__icontains=s)
                events = []
                for venue in venues:
                    eventlist = Event.objects.filter(venue=venue,status="paid")
                    for event in eventlist:
                        events.append(event)
            except Venue.DoesNotExist:
                events = None
        elif searchby == 'organizer':
            try:
                organizers = Organizer.objects.filter(name__icontains=s)
                events = []
                for organizer in organizers:
                    eventlist = Event.objects.filter(organizer=organizer, status="paid")
                    for event in eventlist:
                        events.append(event)
            except Organizer.DoesNotExist:
                try:
                    users = User.objects.filter(name__icontains=s)
                    events = []
                    for user in users:
                        eventlist = Event.objects.filter(user=user)
                        for event in eventlist:
                            events.append(event)
                except User.DoesNotExist:
                    events = None
        else:
            events = None
        return render(re, 'searchevent.html', {'events': events})
    return render(re, 'searchevent.html')

def userevents(re):
    if 'user' in re.session:
        user=User.objects.get(username=re.session['user'])
        tickets = Ticket.objects.filter(user=user)
        p_events=[]
        for i in tickets:
            p_events.append(i.event)
        p_events=set(p_events)
        return render(re,'userevents.html',{'events':p_events})
    messages.warning(re, "User not logged in ")
    return redirect(login)

def logout(re):
    if 'user' in re.session:
        re.session.flush()
        return redirect(index)
    if 'admin' in re.session:
        re.session.flush()
        return redirect(index)

def userprofile(re):
    if 'user' in re.session:
        c = User.objects.get(username=re.session['user'])
        return render(re,'userprofile.html',{'user':c})
    return redirect(login)

def edituserprofile(request):
    if 'user' in request.session:
        try:
            user = User.objects.get(username=request.session['user'])
        except User.DoesNotExist:
            messages.error(request, "User not found")
            return redirect('login')

        if request.method == 'POST':
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone_number = request.POST.get('phone_number')
            address = request.POST.get('address')
            district = request.POST.get('district')
            pincode = request.POST.get('pincode')
            date_of_birth = request.POST.get('date_of_birth')
            age = request.POST.get('age')
            username = request.POST.get('username')
            password = request.POST.get('password')

            # Check for uniqueness
            existing_email = User.objects.filter(email=email).exclude(username=user.username).exists()
            existing_username = User.objects.filter(username=username).exclude(username=user.username).exists()
            existing_phone_number = User.objects.filter(phone_number=phone_number).exclude(username=user.username).exists()

            if existing_email:
                messages.warning(request, "Email already registered")
            elif existing_username:
                messages.warning(request, "Username already exists")
            elif existing_phone_number:
                messages.warning(request, "Phone number already exists")
            else:
                # Update fields if there are no conflicts
                user.name = name
                user.email = email
                user.phone_number = phone_number
                user.address = address
                user.district = district
                user.pincode = pincode
                user.date_of_birth = date_of_birth
                user.age = age
                user.username = username
                user.password = password

                try:
                    user.save()  # Save the updates
                    messages.success(request, 'Update Successful')
                except Exception as e:
                    messages.error(request, f"Update failed: {str(e)}")

        return render(request, 'edituserprofile.html', {'user': user})

    messages.error(request, "User not logged in")
    return redirect('login')


def organizerprofile(re):
    if 'user' in re.session:
        try:
            c = Organizer.objects.get(username=re.session['user'])
        except:
            return redirect(login)
        return render(re,'organizerprofile.html',{'organizer':c})
    return redirect(login)

def editorganizerprofile(request):
    if 'user' in request.session:
        try:
            organizer = Organizer.objects.get(username=request.session['user'])
        except Organizer.DoesNotExist:
            messages.warning(request, "Organizer not found")
            return redirect(login)

        if request.method == "POST":
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone_number = request.POST.get('phone_number')
            address = request.POST.get('address')
            licenseid = request.POST.get('licenseid')
            username = request.POST.get('username')
            password = request.POST.get('password')

            organizer.name = name
            organizer.email = email
            organizer.phone_number = phone_number
            organizer.address = address
            organizer.licenseid = licenseid
            organizer.username = username
            if password:
                organizer.password = password

            # Check for uniqueness
            existing_email = Organizer.objects.filter(email=email).exclude(id=organizer.id).exists()
            existing_username = Organizer.objects.filter(username=username).exclude(id=organizer.id).exists()
            existing_phone_number = Organizer.objects.filter(phone_number=phone_number).exclude(id=organizer.id).exists()

            if existing_email:
                messages.warning(request, "Email already registered")
            elif existing_username:
                messages.warning(request, "Username already exists")
            elif existing_phone_number:
                messages.warning(request, "Phone number already exists")
            else:

                try:
                    organizer.save()  # Save the updates
                    messages.success(request, 'Update Successful')
                except Exception as e:
                    messages.warning(request, f"Update error: {str(e)}")

        return render(request, 'editorganizerprofile.html', {'organizer': organizer})

    messages.warning(request, "User not logged in")
    return redirect(login)

def createeventuser(re):
    if 'user' in re.session:
        try:
            c = User.objects.get(username=re.session['user'])
        except Exception:
            messages.error(re, "Can't access user ")
            return redirect(login)
        if re.method=='POST':

            name=re.POST.get('name')
            image=re.FILES.get('image')
            categoryid=re.POST.get('category')
            user=c
            venueid=re.POST.get('venueid')
            ticketprice=re.POST.get('ticketprice')
            maxparticipants=re.POST.get('maxparticipants')
            start=re.POST.get('start')
            end=re.POST.get('end')
            details=re.POST.get('details')

            start_date = date.today()
            try:
                start_date = datetime.strptime(start, '%Y-%m-%dT%H:%M').date()  # Assuming 'start' is in 'YYYY-MM-DDT%H:%M' format
            except ValueError:
                # Handle the error if the date format is incorrect
                messages.warning(re,'Invalid date format. start date : ' + start)
                categories = EventCategory.objects.filter(level='userandorganizer')
                venues = Venue.objects.all()
                return render(re, 'createeventuser.html', {'user': c, 'categories': categories, 'venues': venues})
            # Step 4: Define the date range (start_date and the day after)
            start_date_next_day = start_date + timedelta(days=1)
            # Step 5: Filter events based on the date range
            venue=Venue.objects.get(id=venueid)
            category=EventCategory.objects.get(id=categoryid)
            events = Event.objects.filter(start__date__in=[start_date, start_date_next_day],venue=venue)
            # Convert string to datetime
            start_datetimeb = datetime.strptime(start, '%Y-%m-%dT%H:%M')
            end_datetimeb = datetime.strptime(end, '%Y-%m-%dT%H:%M')

            start_datetime = timezone.make_aware(start_datetimeb, timezone.get_current_timezone())
            end_datetime = timezone.make_aware(end_datetimeb, timezone.get_current_timezone())

            # Step 1: Check if the duration between start and end is at least 10 minutes
            duration = end_datetime - start_datetime
            if duration < timedelta(minutes=10):
                messages.warning(re,'Event Duration should be atleast 10 minutes')
            elif not is_timeslot_available(start_datetime, end_datetime, events):
                messages.warning(re,'Timeslot not available.')
            elif venue.maxparticipants<int(maxparticipants):
                messages.warning(re,'Maximum Partipants exceeding the Venue Limit')
            else:
                price_per_hour = category.priceperhour
                total_price = calculatetotalprice(start_datetime, end_datetime, price_per_hour)
                price = total_price
                obj = Event.objects.create(
                    name=name,image=image,
                    category=category,
                    user=c,
                    venue=venue,
                    ticketprice=ticketprice,
                    maxparticipants=maxparticipants,
                    start = start_datetime,
                    end = end_datetime,
                    details = details,
                    price = price,
                )
                obj.save()
                # before = ".\nBefore:" + str(start_datetimeb) + str(end_datetimeb)
                # after = ".\nAfter:" + str(start_datetime) + str(end_datetime)
                messages.success(re,'Event Created Successfully. Wait for approval and Pay ')
                categories = EventCategory.objects.filter(level='userandorganizer')
                venues = Venue.objects.all()
                return render(re, 'createeventuser.html', {'user': c, 'categories': categories, 'venues': venues})
            categories = EventCategory.objects.filter(level='userandorganizer')
            venues = Venue.objects.all()
            return render(re, 'createeventuser.html', {'user': c, 'categories': categories, 'venues': venues})
        else:
            categories=EventCategory.objects.filter(level='userandorganizer')
            venues=Venue.objects.all()
            return render(re,'createeventuser.html',{'user':c,'categories':categories,'venues':venues})
    return redirect(login)


def createeventorganizer(re):
    if 'user' in re.session:
        try:
            c = Organizer.objects.get(username=re.session['user'])
        except Exception:
            return redirect(login)
        if re.method=='POST':

            name=re.POST.get('name')
            image=re.FILES.get('image')
            categoryid=re.POST.get('category')
            user=c
            venueid=re.POST.get('venueid')
            ticketprice=re.POST.get('ticketprice')
            maxparticipants=re.POST.get('maxparticipants')
            start=re.POST.get('start')
            end=re.POST.get('end')
            details=re.POST.get('details')
            errorfound=0

            start_date = date.today()
            try:
                start_date = datetime.strptime(start, '%Y-%m-%dT%H:%M').date()  # Assuming 'start' is in 'YYYY-MM-DD' format
            except ValueError:
                # Handle the error if the date format is incorrect
                messages.warning(re,'Invalid date format')
                errorfound = 1
                categories = EventCategory.objects.all()
                venues = Venue.objects.all()
                return render(re, 'createeventorganizer.html', {'user': c, 'categories': categories, 'venues': venues})
            # Step 4: Define the date range (start_date and the day after)
            start_date_next_day = start_date + timedelta(days=1)
            # Step 5: Filter events based on the date range
            venue=Venue.objects.get(id=venueid)
            category=EventCategory.objects.get(id=categoryid)
            events = Event.objects.filter(start__date__in=[start_date, start_date_next_day],venue=venue)
            # Convert string to datetime
            start_datetimeb = datetime.strptime(start, '%Y-%m-%dT%H:%M')
            end_datetimeb = datetime.strptime(end, '%Y-%m-%dT%H:%M')

            start_datetime = timezone.make_aware(start_datetimeb, timezone.get_current_timezone())
            end_datetime = timezone.make_aware(end_datetimeb, timezone.get_current_timezone())

            # Step 1: Check if the duration between start and end is at least 10 minutes
            duration = end_datetime - start_datetime
            if duration < timedelta(minutes=10):
                messages.warning(re,'Event Duration should be atleast 10 minutes')
                errorfound = 1
            elif not is_timeslot_available(start_datetime, end_datetime, events):
                messages.warning(re,'Timeslot not available.')
                errorfound = 1
            elif venue.maxparticipants<int(maxparticipants):
                messages.warning(re,'Maximum Partipants exceeding the Venue Limit')
                errorfound = 1
            else:
                price_per_hour = category.priceperhour
                total_price = calculatetotalprice(start_datetime, end_datetime, price_per_hour)
                price = total_price
                obj = Event.objects.create(
                    name=name,image=image,
                    category=category,
                    organizer=c,
                    venue=venue,
                    ticketprice=ticketprice,
                    maxparticipants=maxparticipants,
                    start = start_datetime,
                    end = end_datetime,
                    details = details,
                    price=price,
                )
                obj.save()
                messages.warning(re,'Event Created Successfully. Wait for approval and Pay')
                categories = EventCategory.objects.all()
                venues = Venue.objects.all()
                return render(re, 'createeventorganizer.html', {'user': c, 'categories': categories, 'venues': venues})

            categories = EventCategory.objects.all()
            venues = Venue.objects.all()
            return render(re, 'createeventorganizer.html', {'user': c, 'categories': categories, 'venues': venues})
        else:
            categories=EventCategory.objects.all()
            venues=Venue.objects.all()
            return render(re,'createeventorganizer.html',{'user':c,'categories':categories,'venues':venues})
    return redirect(login)

def is_timeslot_available(start_datetime, end_datetime, events):
    # Step 2: Assign new start and end times
    new_start = start_datetime - timedelta(hours=1)
    new_end = end_datetime + timedelta(hours=1)
    # Step 3: Iterate over existing events to check for time conflicts
    for event in events:
        temp = new_start
        while temp < new_end:
            # Check if temp is within any event's time range
            if event.start <= temp <= event.end:
                return False
            # Increment temp by 5 minutes
            temp += timedelta(minutes=5)
    # If no conflicts found, return True
    return True

def userownevents(re):
    if 'user' in re.session:
        try:
            c = User.objects.get(username=re.session['user'])
        except Exception:
            return redirect(login)
        updaterejected()
        current_datetime = timezone.now()
        now = current_datetime

        len1 = 0
        len2 = 0
        len3 = 0
        events = Event.objects.filter(user=c)
        for event in events:
            if event.start <= now and event.end >= now:
                len1 += 1
            elif event.start > now:
                len2 += 1
            elif event.end < now:
                len3 += 1
        status_values = ['pending', 'approved', 'rejected', 'paid', 'cancelled']
        venues = Venue.objects.all()
        categories = EventCategory.objects.all()
        return render(re,'userownevents.html',{'events':events,'now':now,'len1':len1,'len2':len2,'len3':len3,'status_values':status_values,'venues':venues,'categories':categories})
    messages.warning(re,"User not logged in")
    return redirect(login)

def eventcategories(re):
    if 'admin' in re.session:
        ev_cats=EventCategory.objects.all()
        return render(re,'eventcategories.html',{'eventcategories':ev_cats})
    messages.warning(re,"Admin not logged in")
    return redirect(login)

def addeventcategory(re):
    if 'admin' in re.session:
        if re.method=="POST":
            name = re.POST.get('name')
            level = re.POST.get('level')
            priceperhour = re.POST.get('priceperhour')
            if not (level == "organizer" or level == "userandorganizer"):
                messages.warning(re,"data submission error")
                return render(re, 'addcategory.html')
            obj = EventCategory.objects.create(name=name, level=level, priceperhour=priceperhour)
            obj.save()
            messages.success(re,"data saved")
        return render(re,'addcategory.html')
    messages.warning(re,"Admin not logged in")
    return redirect(login)

def venues(re):
    if 'admin' in re.session:
        venues=Venue.objects.all()
        return render(re,'venues.html',{'venues':venues})
    messages.warning(re,"Admin not logged in")
    return redirect(login)

def addvenue(re):
    if 'admin' in re.session:
        if re.method=="POST":
            name = re.POST.get('name')
            image = re.FILES.get('image')
            address = re.POST.get('address')
            district = re.POST.get('district')
            location = re.POST.get('location')
            gmaplink = re.POST.get('gmaplink')
            pincode = re.POST.get('pincode')
            maxparticipants = re.POST.get('maxparticipants')

            #Pincode validation
            pincode_str = str(pincode)
            err_msg=""
            if len(pincode_str)!=6:
                err_msg+="Pincode length should be 6"
            if not pincode_str.isnumeric():
                err_msg+=".\nPincode should be of digits"
            if len(err_msg)>0:
                messages.warning(re,err_msg)
                return render(re, 'addvenue.html')

            #maxparticipants validation
            try:
                t=int(maxparticipants)
            except:
                messages.warning(re,"maximum participants should be number")
                return render(re, 'addvenue.html')
            if int(maxparticipants) < 1:
                messages.warning(re,"maximum participants should be atleast 1")
                return render(re, 'addvenue.html')

            obj = Venue.objects.create(name=name,image=image, address=address, district=district, location=location, pincode=pincode, gmaplink =gmaplink, maxparticipants=maxparticipants)
            obj.save()
            messages.success(re,"Data saved")
            return render(re,'addvenue.html')
        else:
            return render(re,'addvenue.html')
    messages.warning(re,"Admin not logged in")
    return redirect(login)

def organizerevents(re):
    if 'user' in re.session:
        try:
            c = Organizer.objects.get(username=re.session['user'])
        except Exception:
            return redirect(login)
        updaterejected()
        current_datetime = timezone.now()
        now = current_datetime

        len1 = 0
        len2 = 0
        len3 = 0
        events = Event.objects.filter(organizer=c)
        for event in events:
            if event.start <= now and event.end >= now:
                len1 += 1
            elif event.start > now:
                len2 += 1
            elif event.end < now:
                len3 += 1
        status_values = ['pending', 'approved', 'rejected', 'paid', 'cancelled']
        venues = Venue.objects.all()
        categories = EventCategory.objects.all()
        return render(re, 'organizerevents.html', {'events': events, 'now': now, 'len1': len1, 'len2': len2, 'len3': len3,'status_values': status_values, 'venues': venues,'categories': categories})
    messages.warning(re,"Organizer not logged in")
    return redirect(login)

def updaterejected():
    current_datetime = timezone.now()
    now = current_datetime
    events = Event.objects.filter(status='approved')
    # Iterate through events
    for event in events:
        # Check if the approved date is more than or equal to 24 hours ago
        if (event.approveddate is not None) and (event.approveddate <= current_datetime - timedelta(hours=24)):
            # Update the event's status to 'rejected'
            event.status = 'rejected'
            event.statusreason = 'Rejected by not Paying within 24Hrs'
            event.save()  # Save the updated event status

def events(re):
    if 'admin' in re.session:
        updaterejected()
        current_datetime = timezone.now()
        now = current_datetime

        len1=0
        len2=0
        len3=0
        events=Event.objects.all()
        for event in events:
            if event.start <= now and event.end >= now:
                len1+=1
            elif event.start > now:
                len2+=1
            elif event.end < now:
                len3+=1
        status_values=['pending','approved','rejected','paid','cancelled']
        venues=Venue.objects.all()
        organizers=Organizer.objects.all()
        categories=EventCategory.objects.all()

        return render(re,'events.html',{'events':events,'now': current_datetime,'len1':len1,'len2':len2,'len3':len3,'status_values':status_values,'venues':venues,'organizers':organizers,'categories':categories})
    messages.warning(re,"Admin not logged in")
    return redirect(login)

def vieworganizers(re):
    if 'admin' in re.session:
        organizers = Organizer.objects.all()
        return render(re, 'vieworganizers.html', {'organizers': organizers})
    messages.warning(re,"Admin not logged in")
    return redirect(login)

def approveevent(request, d):
    if 'admin' in request.session:
        updaterejected()  # Assuming this is defined elsewhere in your code

        try:
            event = Event.objects.get(id=d)
        except Event.DoesNotExist:
            messages.warning(request, "Event does not exist")
            return redirect(events)

        current_datetime = timezone.now()  # Call timezone.now() to get the current datetime

        if event.status == 'pending':
            event.status = 'approved'
            event.statusreason = 'Approved by Admin'
            event.approvedbyadmin = True
            event.approveddate = current_datetime  # Assign the current datetime
            event.save()

            messages.success(request, "Event Approved")
        else:
            messages.warning(request, "Event is not Pending")

        return redirect(events)  # Use 'events' as the URL name for redirection

    messages.warning(request, "Admin not logged in")
    return redirect(login)


def disapproveevent(re,d):
    if 'admin' in re.session:
        try:
            event=Event.objects.get(id=d)
        except Exception:
            return redirect(events)
        else:
            event.approvedbyadmin=False
            event.save()
            messages.success(re,re,'Event Disapproved')
            return redirect(events)
    messages.warning(re,"Admin not logged in")
    return redirect(login)

def singleevent(re,d):
    try:
        event = Event.objects.get(id=d)
    except Exception:
        messages.warning(re,"Event not existing")
        return redirect(searchevent)
    else:
        return render(re,'singleevent.html',{'event' : event})

def singleeventadmin(re,d):
    try:
        event = Event.objects.get(id=d)
    except Exception:
        messages.warning(re,"Event not existing")
        return redirect(events)
    else:
        return render(re,'singleeventadmin.html',{'event' : event})

def singleeventorganizer(re,d):
    try:
        event = Event.objects.get(id=d)
    except Exception:
        messages.warning(re,"Event not existing")
        return redirect(events)
    else:
        return render(re,'singleeventorganizer.html',{'event' : event})


def calculatetotalprice(start_datetime, end_datetime, price_per_hour):
    currentdate = start_datetime.date()  # Get only the date part of the start
    enddate = end_datetime.date()  # Get only the date part of the end
    total_hours = 0

    # If the event starts and ends on the same day
    if currentdate == enddate:
        # Calculate the time gap in hours and minutes between the start and end time
        timegap = end_datetime - start_datetime
        hours, remainder = divmod(timegap.seconds, 3600)
        minutes = remainder // 60
        # Convert minutes to hours fraction and add to hours
        total_hours = hours + (minutes / 60)

    # If the event spans multiple days
    else:
        while currentdate != enddate:
            # Add 15 hours per day (assuming 6 AM to 9 PM)
            total_hours += 15
            currentdate += timedelta(days=1)  # Move to the next day

        # Calculate the time from event start time to 9 PM (15 hours)
        start_of_day = datetime.combine(currentdate, time(6, 0))  # 6 AM
        timegap = end_datetime - start_of_day
        hours, remainder = divmod(timegap.seconds, 3600)
        minutes = remainder // 60
        # Convert minutes to hours fraction and add to total_hours
        total_hours += hours + (minutes / 60)

    # Calculate total price based on total hours and price per hour
    total_price = price_per_hour * total_hours
    return total_price



def eventsbyvenue(re,d):
    if 'admin' in re.session:
        updaterejected()
        current_datetime = timezone.now()
        now = current_datetime

        len1 = 0
        len2 = 0
        len3 = 0
        events = Event.objects.all()
        for event in events:
            if event.start <= now and event.end >= now:
                len1 += 1
            elif event.start > now:
                len2 += 1
            elif event.end < now:
                len3 += 1
        status_values = ['pending', 'approved', 'rejected', 'paid', 'cancelled']
        venues = Venue.objects.all()
        categories = EventCategory.objects.all()
        return render(re, 'userownevents.html', {'events': events, 'now': now, 'len1': len1, 'len2': len2, 'len3': len3,'status_values': status_values, 'venues': venues, 'categories': categories})
    messages.warning(re,"Admin Not Logged in")
    return redirect(login)

def rejectevent(re,d):
    if 'admin' in re.session:

        updaterejected()

        event = Event.objects.get(id=d)
        if event.status=='pending':
            event.status='rejected'
            event.statusreason='Rejected by Admin'
            event.save()
            messages.warning(re,"Event Rejected")
        elif event.status=='approved':
            if not event.paid:
                event.status='rejected'
                event.statusreason='Rejected by Admin'
                event.save()
                messages.warning(re,"Event Rejected")
        else:
            messages.warning(re,'Event paid or cancelled')
        return redirect(events)
    messages.warning(re,"Admin Not Logged in")
    return redirect(login)

def canceleventorganizer(re,d):
    current_datetime=timezone.now()
    updaterejected()

    if 'user' in re.session:
        try:
            event = Event.objects.get(id=d)
        except Exception:
            messages.warning(re,"Event doesn't exists")
            return redirect(organizerevents)
        try:
            c = Organizer.objects.get(username=re.session['user'])
        except Exception:
            messages.warning(re,"Organizer error")
            return redirect(login)

        if(event.organizer!=c):
            messages.warning(re,"Event not created by you \n Event.organizer : "+" \n You : "+c.name)
            return redirect(organizerevents)

        if (event.status=='cancelled' or event.status=='rejected'):
            messages.warning(re, "Cancel Not Possible, Event is " + event.status)
            return redirect(organizerevents)
        refund=0
        if(event.payed):
            current_datetime = timezone.now()
            eventstart = event.start
            if current_datetime <= eventstart - timedelta(hours=24*20):
                refund=100
            elif current_datetime <= eventstart - timedelta(hours=24*10):
                refund=75
            elif current_datetime <= eventstart - timedelta(hours=24*5):
                refund=50
            elif current_datetime <= eventstart - timedelta(hours=24*2):
                refund=0
        return render(re,'canceleventorganizer.html',{'refund':refund,'event':event,'organizer':c,'current_datetime':current_datetime})
    else:
        messages.warning(re, "Organizer Not Logged in")
        return redirect(login)

def canceleventnopayorganizer(re,d):
    if 'user' in re.session:
        event=Event.objects.get(id=d)
        event.status="cancelled"
        event.statusreason="Event cancelled by Organizer"
        event.save()
        return redirect(organizerevents)
    messages.warning(re, "Organizer Not Logged in")
    return redirect(login)

def canceleventuser(re,d):

    updaterejected()

    if 'user' in re.session:
        try:
            event = Event.objects.get(id=d)
        except Exception:
            messages.warning(re,"Event doesn't exists")
            return redirect(userownevents)
        try:
            c = User.objects.get(username=re.session['user'])
        except Exception:
            messages.warning(re,"User error")
            return redirect(login)

        if(event.user!=c):
            messages.warning(re,"Event not created by you")
            return redirect(userownevents)

        if (event.status=='cancelled' or event.status=='rejected'):
            messages.warning(re, "Cancel Not Possible, Event is " + event.status)
            return redirect(userownevents)

        refund=0
        if(event.payed):
            current_datetime = timezone.now()
            eventstart = event.start
            if current_datetime <= eventstart - timedelta(hours=24*20):
                refund=100
            elif current_datetime <= eventstart - timedelta(hours=24*10):
                refund=75
            elif current_datetime <= eventstart - timedelta(hours=24*5):
                refund=50
            elif current_datetime <= eventstart - timedelta(hours=24*2):
                refund=0
        return render(re,'canceleventuser.html',{'refund':refund,'event':event,'user':c})
    else:
        messages.warning(re, "User Not Logged in")
        return redirect(login)

def canceleventnopayuser(re,d):
    if 'user' in re.session:
        event=Event.objects.get(id=d)
        event.status="cancelled"
        event.statusreason = "Event cancelled by Organizer"
        event.save()
        messages.success(re, "Event Cancelled")
        return redirect(organizerevents)
    messages.warning(re, "User Not Logged in")
    return redirect(login)


def forgot_password_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
        except:
            messages.info(request,"Email id not registered")
            return redirect(forgot_password_user)
        # Generate and save a unique token
        token = get_random_string(length=4)
        PasswordReset.objects.create(user=user, token=token)

        # Send email with reset link
        reset_link = f'http://127.0.0.1:8000/reset/{token}'
        try:
            send_mail('Reset Your Password', f'Click the link to reset your password: {reset_link}','settings.EMAIL_HOST_USER', [email],fail_silently=False)
            # return render(request, 'emailsent.html')
            messages.info(request,"Password Reset Email has been sent")
            return redirect(forgot_password_user)
        except:
            messages.info(request,"Network connection failed")
            return redirect(forgot_password_user)
    return render(request, 'forgot_password.html')

def reset_password_user(request, token):
    # Verify token and reset the password
    print(token)
    password_reset = PasswordReset.objects.get(token=token)
    # usr = User.objects.get(id=password_reset.user_id)
    if request.method == 'POST':
        new_password = request.POST.get('newpassword')
        repeat_password = request.POST.get('cpassword')
        if repeat_password == new_password:
            password_reset.user.password=new_password
            password_reset.user.save()
            # password_reset.delete()
            return redirect(login)
    return render(request, 'reset_password.html',{'token':token})

def forgot_password_organizer(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            organizer = Organizer.objects.get(email=email)
        except:
            messages.info(request,"Email id not registered")
            return redirect(forgot_password_user)
        # Generate and save a unique token
        token = get_random_string(length=4)
        PasswordResetOrganizer.objects.create(organizer=organizer, token=token)

        # Send email with reset link
        reset_link = f'http://127.0.0.1:8000/resetorganizer/{token}'
        try:
            send_mail('Reset Your Password', f'Click the link to reset your password: {reset_link}','settings.EMAIL_HOST_USER', [email],fail_silently=False)
            # return render(request, 'emailsent.html')
            messages.info(request, "Password Reset Email has been sent")
            return redirect(forgot_password_organizer)
        except:
            messages.info(request,"Network connection failed")
            return redirect(forgot_password_organizer)

    return render(request, 'forgotpasswordorg.html')

def reset_password_organizer(request, token):
    # Verify token and reset the password
    print(token)
    password_reset = PasswordResetOrganizer.objects.get(token=token)
    # usr = User.objects.get(id=password_reset.user_id)
    if request.method == 'POST':
        new_password = request.POST.get('newpassword')
        repeat_password = request.POST.get('cpassword')
        if repeat_password == new_password:
            password_reset.organizer.password=new_password
            password_reset.organizer.save()
            # password_reset.delete()
            messages.info(request, "New password has been set. Please login")
            return redirect(login)
    return render(request, 'reset_password.html',{'token':token})


def payeventuser(re,d):
    if 'user' in re.session:
        try:
            event = Event.objects.get(id=d)
        except Exception:
            messages.warning(re,"Event doesn't exists")
            return redirect(singleevent, d=event.id)
        try:
            c = User.objects.get(username=re.session['user'])
        except Exception:
            messages.warning(re,"User error")
            return redirect(login)

        if(event.user!=c):
            messages.warning(re,"Event not created by you")
            return redirect(singleevent,d=event.id)
        category = event.category
        price_per_hour = category.priceperhour
        start_datetime = event.start
        end_datetime = event.end
        total_price = calculatetotalprice(start_datetime,end_datetime,price_per_hour)
        event.price=total_price
        return render(re,'payeventuser.html',{'event':event,'user':c,'totalprice':total_price,'priceperhour':price_per_hour})
    messages.warning(re,"User or Organizer not Logged in")
    return redirect(login)

def payeventorganizer(re,d):
    if 'user' in re.session:
        try:
            event = Event.objects.get(id=d)
        except Exception:
            messages.warning(re,"Event doesn't exists")
            return redirect(singleevent, d=event.id)
        try:
            c = Organizer.objects.get(username=re.session['user'])
        except Exception:
            messages.warning(re,"Organizer error")
            return redirect(login)

        if(event.organizer!=c):
            messages.warning(re,"Event not created by you")
            return redirect(singleevent,d=event.id)
        category = event.category
        price_per_hour = category.priceperhour
        start_datetime = event.start
        end_datetime = event.end
        total_price = calculatetotalprice(start_datetime,end_datetime,price_per_hour)
        event.price=total_price
        return render(re,'payeventorganizer.html',{'event':event,'organizer':c,'totalprice':total_price,'priceperhour':price_per_hour})
    messages.warning(re,"User or Organizer not Logged in")
    return redirect(login)

def bookevent(re,d):
    if 'user' in re.session:
        c = User.objects.get(username=re.session['user'])
        event = Event.objects.get(id=d)
        if event.maxparticipants <= event.participants:
            messages.warning(re,'Participants Filled')
        return render(re,'bookevent.html',{'event':event,'user':c})
    messages.warning(re,"User not logged in")
    return redirect(login)

# ---------------------------- SINGLE BOOKING ---------------------------
# def singles(request, d):
#     if 'user' in request.session:
#         user = User.objects.get(username=request.session['user'])
#         event = Event.objects.get(pk=d)
#         return render(request, 'singlepay.html', {'data': user, 'pdata': event})
#     return redirect(userhome)
#
# def single_booking(request, event_id):
#     if 'user' not in request.session:
#         return redirect(userhome)
#
#     event = get_object_or_404(Event, pk=event_id)
#     user = get_object_or_404(User, username=request.session['user'])
#     # event = mycart.objects.filter(usr=user).first()
#
#
#     if request.method == "POST":
#         so_fname = request.POST.get('sofname', '')
#         so_lname = request.POST.get('solname', '')
#         so_email = request.POST.get('semail', '')
#         so_phone = int(request.POST.get('sphone', 10))
#         so_address = request.POST.get('sadrs', '')
#         so_district = request.POST.get('sdistrict', '')
#         so_pincode = int(request.POST.get('spincode', 6))
#         add_message = request.POST.get('add_det', '')
#         quantity = int(request.POST.get('singleqty', 1))
#         total_price = float(request.POST.get('total', 0))
#         paymode = request.POST.get('payment_mode', '')
#
#         total_price=event.price
#
#         order_id = 'ordid' + str(random.randint(1111111, 9999999))
#         while Order.objects.filter(order_id=order_id).exists():
#             order_id = 'ordid' + str(random.randint(1111111, 9999999))
#
#         tracking_no = 'bag' + str(random.randint(1111111, 9999999))
#         while Order.objects.filter(tracking_no=tracking_no).exists():
#             tracking_no = 'bag' + str(random.randint(1111111, 9999999))
#
#         single_booking = Order.objects.create(
#             user=user,
#             event=event,
#             so_fname=so_fname,
#             so_lname=so_lname,
#             so_email=so_email,
#             so_phone=so_phone,
#             so_address=so_address,
#             so_district=so_district,
#             so_pincode=so_pincode,
#             add_message=add_message,
#             quantity=quantity,
#             status='Pending',
#             payment_mode=paymode,
#             payment_id=None,
#             order_id=order_id,
#             tracking_no=tracking_no,
#             total_price=total_price,
#         )
#         single_booking.save()
#
#         messages.success(request, 'Your order has been placed successfully')
#
#         # if paymode == 'RazorPay':
#         #     return redirect('single_booking', price=total_price)
#         #     # return JsonResponse({'status': 'Your order has been placed successfully'})
#         #
#         # return redirect('single_booking', product_id=product.id)
#
#     return redirect(userhome)
#
# # razorpay
#
def single_razor(request, event_id,type):
    event = get_object_or_404(Event, pk=event_id)
    try:
        user = User.objects.get(username=request.session['user'])
    except User.DoesNotExist:
        user = User.objects.get(username='nouser')
    try:
        organizer = Organizer.objects.get(username=request.session['user'])
    except Organizer.DoesNotExist:
        organizer = Organizer.objects.get(username='noorganizer')


    # crt = mycart.objects.filter(usr=user).first()


    if request.method == "POST":
        print("hello")
        so_fname = request.POST.get('sofname', '')
        # so_lname = request.POST.get('solname', '')
        so_email = request.POST.get('semail', '')
        so_phone = int(request.POST.get('sphone', 10))
        so_address = request.POST.get('sadrs', '')
        so_district = request.POST.get('sdistrict', '')
        so_city = request.POST.get('scity', '')
        so_pincode = int(request.POST.get('spincode', 6))
        add_message = request.POST.get('notes', '')
        quantity = int(request.POST.get('singleqty', 1))
        total_price = float(request.POST.get('total', 0))
        paymode = request.POST.get('payment_mode', '')
        print(paymode,total_price)
        nopersons=request.POST.get('num_persons')


        order_id = 'ordid' + str(random.randint(1111111, 9999999))
        while Order.objects.filter(order_id=order_id).exists():
            order_id = 'ordid' + str(random.randint(1111111, 9999999))

        tracking_no = 'bag' + str(random.randint(1111111, 9999999))
        while Order.objects.filter(tracking_no=tracking_no).exists():
            tracking_no = 'bag' + str(random.randint(1111111, 9999999))

        single_booking = Order.objects.create(
            user=user,
            organizer=organizer,
            event=event,
            so_fname=so_fname,
            # so_lname=so_lname,
            so_email=so_email,
            so_phone=so_phone,
            so_address=so_address,
            so_district=so_district,
            so_pincode=so_pincode,
            add_message=add_message,
            quantity=quantity,
            status='Pending',
            type=type,
            payment_mode=paymode,
            payment_id=None,
            order_id=order_id,
            tracking_no=tracking_no,
            total_price=total_price,
        )
        # if paymode == 'RazorPay':
        if type=='bookevent':
            if event.participants+int(nopersons)>event.maxparticipants:
                messages.error(request,"Exceeding the limit")
                return redirect(bookevent,d=event_id)
            else:
                ticketprice=event.ticketprice
                totalticketprice=int(nopersons)*ticketprice
                single_booking.ticketprice=ticketprice
                single_booking.quantity=int(nopersons)
                single_booking.total_price=totalticketprice
            single_booking.save()
            return redirect(razorpaycheck, single_booking.total_price)
        single_booking.save()
        return redirect(razorpaycheck,event.price)
    #     return JsonResponse({'status': 'Your order has been placed successfully'})
    #
    # return redirect(usr_home)


def razorpaycheck(request,price):
    if 'user' in request.session:
        try:
            user = User.objects.get(username=request.session['user'])
            s = Order.objects.filter(user=user)
        except Exception:
            user = User.objects.get(username='nouser')
        try:
            organizer = Organizer.objects.get(username=request.session['user'])
            s = Order.objects.filter(organizer=organizer)
        except Organizer.DoesNotExist:
            organizer = Organizer.objects.get(username='noorganizer')
        t = price*100
        return render(request, "payment.html", {'amount': t})
    return render(request, "payment.html")

def success(re):
    orders=Order.objects.all()
    for order in orders:
        if(order.type=='payeventuser' or order.type == 'payeventorganizer'):
            order.event.status='paid'
            order.event.payed=True
            order.event.save()
        if(order.type=='bookevent'):
            user=order.user
            event=order.event
            ticket_id = 'tktid' + str(random.randint(1111111, 9999999))
            while Ticket.objects.filter(ticket_id=ticket_id).exists():
                ticket_id = 'ordid' + str(random.randint(1111111, 9999999))
            timestamp=order.created_at
            npersons=order.quantity
            total_price=order.total_price
            payment_id=order.order_id
            if not Ticket.objects.filter(payment_id=payment_id).exists():
                t=Ticket.objects.create(user=user,event=event,ticket_id=ticket_id,timestamp=timestamp,npersons=npersons,total_price=total_price,payment_id=payment_id)
                t.save()
        order.save()
    if 'user' in re.session:
        try:
            user = User.objects.get(username=re.session['user'])
            return redirect(showusertickets)
        except Exception:
            organizer = Organizer.objects.get(username=re.session['user'])
            return redirect(organizerevents)
    return render(re,"success.html",{'orders':orders})

def showusertickets(re):
    if 'user' in re.session:
        c = User.objects.get(username=re.session['user'])
        tickets= Ticket.objects.filter(user=c)
        current_datetime = timezone.now()
        for ticket in tickets:
            if (ticket.timestamp is not None) and (ticket.timestamp <= current_datetime - timedelta(hours=24)):
                ticket.tempcancellable=False
        return render(re,'showusertickets.html',{'tickets':tickets})
    messages.warning(re,"User not logged in")
    return redirect(login)

def cancelticket(re,d):
    if 'user' in re.session:
        c = User.objects.get(username=re.session['user'])
        ticket= Ticket.objects.get(id=d)
        if ticket.cancelticket==True:
            messages.warning(re,"Ticket Already Cancelled")
            return redirect(showusertickets)
        current_datetime = timezone.now()
        # Check if the date is more than or equal to 24 hours ago
        if (ticket.timestamp is not None) and (ticket.timestamp <= current_datetime - timedelta(hours=24)):
            messages.warning(re,"Cannot cancel after 24 hours")
            return redirect(showusertickets)
        return render(re,'cancelticket.html',{'ticket' : ticket})
    messages.warning(re,"User not logged in")
    return redirect(login)

def cancelticket2(re,d):
    if 'user' in re.session:
        c = User.objects.get(username=re.session['user'])
        ticket= Ticket.objects.get(id=d)
        if ticket.cancelticket==True:
            messages.warning(re,"Ticket Already Cancelled , ticket.cancelticket : "+str(ticket.cancelticket))
            return redirect(showusertickets)
        current_datetime = timezone.now()
        # Check if the date is more than or equal to 24 hours ago
        if (ticket.timestamp is not None) and (ticket.timestamp <= current_datetime - timedelta(hours=24)):
            messages.warning(re,"Cannot cancel after 24 hours")
            return redirect(showusertickets)
        ticket.cancelticket=True
        ticket.save()
        messages.success(re, "Ticket Cancelled")
        ticket = Ticket.objects.get(id=d)
        return redirect('refundticket', d=ticket.id)
    messages.warning(re,"User not logged in")
    return redirect(login)


def refundticket(re, d):
    try:
        ticket = Ticket.objects.get(id=d)

        if ticket.isrefunded == True:
            messages.warning(re, "Ticket already Refunded")
            return redirect(showusertickets)

        if ticket.cancelticket == False:
            messages.warning(re, "Ticket not Cancelled")
            return redirect(showusertickets)

        # Refund the payment (update status)
        ticket.refundid=str(uuid.uuid4())
        ticket.isrefunded=True
        ticket.refunddate=timezone.now()
        ticket.save()
        ticket = Ticket.objects.get(id=d)
        return render(re,"refundticketsuccess.html",{'ticket':ticket})

    except Ticket.DoesNotExist:
        messages.warning(re, "Ticket not Found")
        return redirect(showusertickets)

def refundevent(re, d):
    try:
        event = Event.objects.get(id=d)

        if event.isrefunded == True:
            messages.warning(re, "Event already Refunded")
            return redirect(showusertickets)

        refund = 0
        if (event.payed):
            current_datetime = timezone.now()
            eventstart = event.start
            if current_datetime <= eventstart - timedelta(hours=24 * 20):
                refund = 100
            elif current_datetime <= eventstart - timedelta(hours=24 * 10):
                refund = 75
            elif current_datetime <= eventstart - timedelta(hours=24 * 5):
                refund = 50
            elif current_datetime <= eventstart - timedelta(hours=24 * 2):
                refund = 0

        event.refundprice=event.price*(refund/100)

        # Refund the payment (update status)
        event.refundid=str(uuid.uuid4())
        event.isrefunded=True
        event.refunddate=timezone.now()
        event.status="cancelled"
        event.statusreason="Cancelled by Creator"
        event.save()
        messages.success(re,"Event cancelled")
        event = Event.objects.get(id=d)
        if event.organizer is None:
            #user
            return render(re,"refundeventsuccessuser.html",{'event':event})
        else:
            return render(re,"refundeventsuccessorganizer.html",{'event':event})

    except Event.DoesNotExist:
        messages.warning(re, "Event not Found")
        if 'user' in re.session:
            # user
            if User.objects.get(username=re.session['user']).exists():
                return redirect(userownevents)
            else:
                return redirect(organizerevents)
        else:
            return redirect(login)