from .models import Classroom
import random

room_names = ['Jon', 'Bill', 'Maria', 'Jenny', 'Jack', 'John', 'Paul', 'Kate', 'Ann']
projector = [True, False]

def create_room():
    t = Classroom.objects.create(name=random.choice(room_names), capacity=random.randint(30, 100), projector=random.choice(projector))
    t.save()

def delete_room(id):
    t = Classroom.objects.filter(id=id).delete()