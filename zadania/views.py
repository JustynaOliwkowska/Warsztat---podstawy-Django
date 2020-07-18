from datetime import datetime
import datetime

from django.http import HttpResponse, HttpResponseRedirect
from zadania.models import Classroom, Reservation
from django.shortcuts import render, redirect


# class add_room(View):
#     template_name = 'add_room.html'
#
#     def get(self, request):
#         return render(request, self.template_name)
#
#     def post(self, request):
#         name = request.POST.get("name")
#         capacity = int(request.POST.get("capacity"))
#         projector = request.POST.get("projector")
#         Classroom.objects.create(name=name, capacity=capacity, projector=projector)
#         answer = f"""<html>
#                       <body>
#                         <p>
#                        Class  {name} was added to your database!
#                         </p>
#                       </body>
#                     </html>"""
#         return HttpResponse(answer)

def add_room(request):
    rooms = Classroom.objects.all()
    if request.method == 'GET':
        return render(request, 'add_room.html')

    if request.method == 'POST':
        room_name = request.POST.get('name')
        if room_name == "":
            message = 'Room name cannot be empty'
            return render(request, 'add_room.html', context={'message': message})
        else:
            for room in rooms:
                if room.name == room_name:
                    message = 'Room name already on list! Please choose another one'
                    return render(request, 'add_room.html', context={'message': message})
        room_capacity = int(request.POST.get('capacity'))
        if room_capacity <= 0:
            message = 'Capacity larger than 0'
            return render(request, 'add_room.html', context={'message': message})
    projector = request.POST.get("projector")

    r = Classroom.objects.create(name=room_name, capacity=room_capacity, projector=projector)
    r.save()
    message = 'Room added successfully'
    return render(request, 'add_room.html', context={'message': message})


def show_rooms(request):
    rooms = Classroom.objects.all()
    return render(request, "show_rooms.html", {'rooms': rooms})

def room(request):
    pass

def delete_room(request, id):
    if request.method == 'GET':
        return render(request, 'show_rooms.html',)

    if request.method == 'POST':
        del_room = Classroom.objects.get(id=id)
        # del_room = request.POST.get('id')
        # del_room = Classroom.objects.get('name')
        del_room.delete()
        # del_room.save()
        # z.Classroom.remove(del_room)
        # z.save()
    message = 'Room removed successfully'
    return render(request, 'show_rooms.html', context={'message': message})


def modify_room(request, id):
    if request.method == 'GET':
        return render(request, 'modify_room.html')

    if request.method == 'POST':
        rooms = Classroom.objects.all()
        r_det = Classroom.objects.get(id=id)
        room_name = request.POST.get('name')
        if room_name == "":
            message = 'Room name cannot be empty'
            return render(request, 'modify_room.html', context={'message': message})
        else:
            for room in rooms:
                if room.name == room_name:
                    message = 'Room name already on list! Please choose another one'
                    return render(request, 'modify_room.html', context={'message': message})
        room_capacity = int(request.POST.get('capacity'))
        if room_capacity <= 0:
            message = 'Capacity larger than 0'
            return render(request, 'modify_room.html', context={'message': message})
    projector = request.POST.get("projector")


    r_det.name=room_name
    r_det.capacity=room_capacity
    r_det.projector=projector
    r_det.save()
    message = 'Room modified successfully'
    return render(request, 'modify_room.html', context={'message': message})

def reserve_room(request, id):
    if request.method == 'GET':
        return render(request, 'reserve_room.html')
    else:
        room = Classroom.objects.get(id=id)
        date = request.POST.get("reservation_date")
        comment = request.POST.get("comment")
        if date < str(datetime.date.today()):
            return HttpResponse("Past date!")
        if Reservation.objects.filter(date=date):
            return HttpResponse("Room already reserved!")
        res = Reservation.objects.create(date=date, comment=comment, room_id=room)
        res.save()
        message = 'Room reserved successfully'
        return render(request, 'reserve_room.html', context={'message': message})

def details_room(request, id):
    room = Classroom.objects.get(id=id)
    reservations = room.reservation_set.filter(date__gte=str(datetime.date.today())).order_by('date')
    return render(request, "detailed_room.html", context={"room": room, "reservations": reservations})
