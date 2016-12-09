
from .room import Office,LivingSpace
from .person import Fellow, Staff
class Amity(object):
  """
  Amity class implementing the logic of a facility where it has rooms which can be offices or living spaces. An office can occupy a maximum of 6 people. A living space can inhabit a maximum of 4 people
  A person to be allocated could be a fellow or staff. Staff cannot be allocated living spaces. Fellows have a choice to choose a living space or not.

  """

  offices =[]
  living_spaces =[]
  all_rooms =[]
  fellows=[]
  staff=[]
  all_persons= []

  def create_room(self,name,typ):
    if typ == "O":
      is_used = self.check_if_name_used(name,self.all_rooms)
      if is_used == False:
        new_room = Office(name)
        self.offices.append(new_room)
        self.all_rooms.append(new_room)

        return "Room created succesfully"
      elif is_used == True:
        return "Room could not be created: Room exists!"
      
    elif typ =="L":
      is_used = self.check_if_name_used(name,self.all_rooms)
      if is_used == False:
        new_room = LivingSpace(name)
        self.living_spaces.append(new_room)
        self.all_rooms.append(new_room)

        return "Room created succesfully"
      elif if_used == True:
        return "Room could not be created: name taken!"
      
    else:
      return -1
  def add_person(self,name,phone,email,typ):
    if typ =="F":
      is_used = self.check_if_email_used(email,self.all_persons)
      if is_used == False:
        new_fellow =Fellow(name,phone,email)
        self.all_persons.append(new_fellow)
        self.fellows.append(new_fellow)
        return new_fellow
      else:
        return "Email already used!"
    elif type =="S":
      is_used = self.check_if_email_used(email,self.all_persons)
      if is_used== False:
        new_staff =Staff(name,phone,email)
        self.all_persons.append(new_staff)
        self.staff.append(new_staff)
        return new_staff
      else:
        return "Email already used!"
    else:
      return -1
  def allocate_room(self,person):
    pass
  def reallocate_room(self,person):
    pass




  def check_if_name_used(self,name,items):
    for item in items:
      if item.name == name:
        return True
    return False

  def check_if_email_used(self,email,objects):
    for obj in objects:
      if email == obj.email:
        return True
    return False

  def __del__(self):
    return None
