from django.shortcuts import render, HttpResponse, redirect
from .models import User, Client_details, glass
from datetime import datetime
import datetime as dt
import re
from django.contrib.auth.decorators import login_required


def matchQuery(query, name, phone):
    name = name.upper()
    query = query.upper()
    if query in name or query in phone:
        return True 
    else:
        return False


def LoginPage(request):
    if request.method=="POST":
        phone_no = request.POST.get("phone")
        password = request.POST.get("password")

        try:
            user_details = User.objects.filter(phone=phone_no)
            
            
            if password==user_details[0].password:
                
                return HttpResponse(f"/{str(user_details[0].user_id)}/home/")
            else:
                return HttpResponse("Password Mismatch")

            
        except Exception as e:
            if not user_details:
                return HttpResponse("No user with above credentials")
            elif password!=user_details[0].password:
                return HttpResponse("Incorrect password for above user")
            else:
                return HttpResponse("Invalid credentials")

    return render(request, "login_page.html")

# @login_required(login_url='/')
def Home(request, id):
    user_details = User.objects.filter(user_id=id)
    all_clients = Client_details.objects.all()
    return render(request, "home.html", {"id":id,"add_users":user_details[0].add_users, "authorize":user_details[0].give_access, "all_clients":all_clients})
    
# @login_required(login_url='/')
def addUser(request, id):
    user_details = User.objects.filter(user_id=id)
    all_numbers = list(User.objects.values_list("phone",flat=True))
    

    if request.method=="POST":
        fullname = request.POST.get("fullname","")
        phone = request.POST.get("phone","")
        password1 = request.POST.get("password","")
        allow_add_users = request.POST.get("allow_adding_users","")
        authorize = request.POST.get("allow_authorize","")

        allow_add_users = True if allow_add_users=="on" else False
        authorize = True if authorize=="on" else False
        

        new_user = User(fullname=fullname, password=password1, phone=phone, add_users=allow_add_users, give_access=authorize)
        new_user.save()
        
    return render(request, "add_user.html", {"id":id,"add_users":user_details[0].add_users, "authorize":user_details[0].give_access, "all_numbers":all_numbers})

# @login_required(login_url='/')
def authorizeUsers(request, id):

    user_details = User.objects.filter(user_id=id)
    last_seen = []
    all_users = User.objects.all()
    

    if(request.method=="POST"):
        if "userSubmit" in request.POST:
            userID = request.POST.get("userID")
            allow_add_users = request.POST.get("allow_adding_users","")
            authorize = request.POST.get("allow_authorize","")

            allow_add_users = True if allow_add_users=="on" else False
            authorize = True if authorize=="on" else False
            user_detail = User.objects.get(user_id=userID)
            user_detail.add_users = allow_add_users
            user_detail.give_access = authorize
            user_detail.save()
            return redirect("Authorize Users", id=id)

        elif "searchSubmit" in request.POST:
            query = request.POST.get("searchQuery")
            all_users = User.objects.all()
            query_results = []
            for user in all_users:
                if matchQuery(query, user.fullname, user.phone):
                    query_results.append(user)
                    
            return  render(request, "authorize.html", {"id":id,"add_users":user_details[0].add_users, "authorize":user_details[0].give_access, "all_users":query_results})


    return render(request, "authorize.html", {"id":id,"add_users":user_details[0].add_users, "authorize":user_details[0].give_access, "all_users":all_users})

# @login_required(login_url='/')
def add_new_client(request, id):

    user_details = User.objects.filter(user_id=id)
    
    if request.method=="POST":
        client = request.POST.get("client_name")
        building = request.POST.get("building_name")
        flat = request.POST.get("flat_number")
        new_client = Client_details(client_name=client, building_name=building, flat_no=flat)
        new_client.save()
        new_client_obj = Client_details.objects.get(client_name=client, building_name=building, flat_no=flat)
        r = 1
        i = 1
        number_of_rooms = int(request.POST.get("no_of_rooms"))
        # roomnumbers = 0
        # Loop for total number of rooms
        while(r!=(number_of_rooms+1)):
            
            roomName = request.POST.get("room"+str(i)+"_name")
            no_glasses = request.POST.get("room"+str(i)+"glasses")
            
            # Loop for each room for all glasses
            if roomName!=None and no_glasses!=None:
                j = 1
                g = 1
                while(g!=(int(no_glasses)+1)):
                    glass_details = request.POST.get("room"+str(i)+"_glass"+str(j)+"_details")
                    glass_size1 = request.POST.get("room"+str(i)+"_glass"+str(j)+"_size1")
                    glass_size2 = request.POST.get("room"+str(i)+"_glass"+str(j)+"_size2")
                    glass_polish = request.POST.get("room"+str(i)+"_glass"+str(j)+"_polish")
                    
                    # if there is no glass with id dont increment glass qty
                    if(glass_details!=None):
                        new_glass = glass(client=new_client_obj, room_name=roomName, glass_name = glass_details, glassSize1=glass_size1, glassSize2=glass_size2, polish=glass_polish)
                        new_glass.save()
                        g+=1
                    j+=1
                r+=1   
            i+=1
        return redirect(f"/{id}/home/")
            
    return render(request, "add_new_client.html", {"id":id,"add_users":user_details[0].add_users, "authorize":user_details[0].give_access})

# @login_required(login_url='/')
def show_client_details(request, id, id2):
    user_details = User.objects.filter(user_id=id)
    client_d = Client_details.objects.get(id=id2)
    all_glasses = glass.objects.filter(client=client_d).values_list()
    all_rooms = all_glasses.values_list('room_name').distinct()
    room_names = [x[2] for x in all_glasses]
    rooms_qty_glass = []
    j = 1
    for x in all_rooms:
        rooms_qty_glass.append([j,x[0], room_names.count(x[0])])
        j+=1
    
    if request.method=="POST":
        Client_details.objects.get(id=id2).delete()
        client = request.POST.get("client_name")
        building = request.POST.get("building_name")
        flat = request.POST.get("flat_number")
        new_client = Client_details(client_name=client, building_name=building, flat_no=flat)
        new_client.save()
        new_client_obj = Client_details.objects.get(client_name=client, building_name=building, flat_no=flat)
        r = 1
        i = 1
        number_of_rooms = int(request.POST.get("no_of_rooms"))
        # roomnumbers = 0
        # Loop for total number of rooms
        while(r!=(number_of_rooms+1)):
            
            roomName = request.POST.get("room"+str(i)+"_name")
            no_glasses = request.POST.get("room"+str(i)+"glasses")
            print(roomName, no_glasses)
            
            # Loop for each room for all glasses
            if roomName!=None and no_glasses!=None:
                j = 1
                g = 0
                while(g!=int(no_glasses)):
                    glass_details = request.POST.get("room"+str(i)+"_glass"+str(j)+"_details")
                    glass_size1 = request.POST.get("room"+str(i)+"_glass"+str(j)+"_size1")
                    glass_size2 = request.POST.get("room"+str(i)+"_glass"+str(j)+"_size2")
                    glass_polish = request.POST.get("room"+str(i)+"_glass"+str(j)+"_polish")
                    
                    # if there is no glass with id dont increment glass qty
                    if(glass_details!=None):
                        new_glass = glass(client=new_client_obj, room_name=roomName, glass_name = glass_details, glassSize1=glass_size1, glassSize2=glass_size2, polish=glass_polish)
                        print(roomName, glass_details, glass_size1, glass_size2, glass_polish)
                        new_glass.save()
                        g+=1
                    j+=1
                r+=1   
            i+=1
        return redirect(f"/{id}/home/")
  
    return render(request, "client_details.html", {"id":id,"add_users":user_details[0].add_users, "authorize":user_details[0].give_access, "client":client_d, "rooms_and_no_glass":rooms_qty_glass, "all_glasses":all_glasses, "no_of_rooms":len(all_rooms), "client_id":id2})

def remove_punctuations(string):
    return re.sub('\W+','', string)
# @login_required(login_url='/')
def show_summary(request, id, id2):
    user_details = User.objects.filter(user_id=id)
    all_clients = Client_details.objects.all()
    client_d = Client_details.objects.get(id=id2)
    all_glasses = glass.objects.filter(client=client_d).values_list()
    glass_types = set(map(lambda x:x[3], all_glasses))
    categories = [remove_punctuations(x) for x in glass_types]
    categories = set(categories)
    newlist = [[y for y in all_glasses if remove_punctuations(y[3]).lower()==x.lower()]for x in categories]
    newlist1 = []
    for i in newlist:
        z = []
        for j in i:
            ctr=0
            for x in i:
                if [x[4],x[5],x[6]]==[j[4],j[5],j[6]]:
                    ctr+=1
            z.append([j[4],j[5],j[6],ctr])
        z1 = []
        for elem in z:
            if elem not in z1:
                z1.append(elem)
        newlist1.append([j[3],z1])


    return render(request, "summary.html", {"id":id,"add_users":user_details[0].add_users, "authorize":user_details[0].give_access, "all_clients":all_clients, "client_id":id2,"all_glasses":newlist1})

# @login_required(login_url='/')
def delete_user(request, id, id2):

    user_details = User.objects.filter(user_id=id2)
    
    if request.method=="POST":
        User.objects.get(user_id=id2).delete()
        return redirect(f"/{id}/authorize/")
    return render(request, "confirm_delete_user.html", {"id":id,"name":user_details[0].fullname,"phone":user_details[0].phone})


def delete_client(request, id, id2):

    user_details = Client_details.objects.filter(id=id2)
    
    if request.method=="POST":
        Client_details.objects.get(id=id2).delete()
        return redirect(f"/{id}/home/")
    return render(request, "confirm_delete_client.html", {"id":id,"name":user_details[0].client_name,"address":user_details[0].flat_no+" "+user_details[0].building_name})


