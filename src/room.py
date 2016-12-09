from abc import ABCMeta, abstractmethod
class Room(object):
  __meta__ = ABCMeta
 
  def __init__(self,name ):
    self.name = name
    self.allocated_spaces =0
    self.unallocated_spaces = self.capacity -self.allocated_spaces

  @property
  def _is_full(self):
      if self.allocated_spaces == self.capacity:
        print("it is true!!")
        return True
      elif self.allocated_spaces < self.capacity:
        return False
  @property
  def _is_empty(self):
    if self.allocated_spaces == 0:
      return True
    else:
      return False
  def allocate_room_space(self):
    if self._is_full==True:
      return -1
    else:
      print("allocationg new")
      self.allocated_spaces += 1
      print ("new allocated")
      self.unallocated_spaces = self.capacity -self.allocated_spaces
      return("Room Allocated")
  def deallocate_room_space(self):
    if self._is_empty:
      rerturn -1
    else:
      self.allocated_spaces =self.allocated_spaces -1
      self.unallocated_spaces = self.capacity - self.allocated_spaces

class LivingSpace(Room):
  capacity = 4
  def __init__(self,room_name):
    super(LivingSpace, self).__init__(room_name)

  @property
  def room_type(self):
    return "LivingSpace"

class Office(Room):
  capacity = 6
  def __init__(self,room_name):
    super(Office, self).__init__(room_name,)

  @property
  def room_type(self):
    return "OfficeSpace"
