import unittest
from src.amity import Amity

class Tdd_Amity(unittest.TestCase):


  def setUp(self):
    self.amity = Amity()
    self.previous_room_count = len(self.amity.all_rooms)

  def test_create_office(self):
    self.assertFalse(check_if_name_used("Kingslanding",self.amity.all_rooms))
    self.amity.create_room('Kingslanding', 'O')
    self.assertTrue(check_if_name_used('Kingslanding',self.amity.all_rooms))
    new_room_count = len(self.amity.all_rooms)
    self.assertEqual(self.previous_room_count + 1, new_room_count)

  def test_create_office_error_if_exists(self):
    self.amity.create_room('Kingslanding', 'O')
    self.assertTrue(check_if_name_used('Kingslanding',self.amity.all_rooms))
    response = self.amity.create_room('Kingslanding', 'O')
    self.assertEqual(response, "Room could not be created: Room exists!")
  
  def test_creating_living_space(self):
    self.assertFalse(check_if_name_used('Winterfell',self.amity.all_rooms)) 
    self.amity.create_room('Winterfell', 'O')
    self.assertTrue(check_if_name_used('Winterfell',self.amity.all_rooms))
    new_room_count = len(self.amity.all_rooms)
    self.assertEqual(self.previous_room_count + 1, new_room_count)
  
  def test_creating_room_with_invalid_room_type(self):
    self.assertTrue("Mereen" not in self.amity.all_rooms)
    sample = self.amity.create_room("Mereen","K")
    self.assertEqual(sample,-1)


  def test_adding_fellows(self):
    self.assertFalse(check_if_email_used("tyrion@got.world",self.amity.all_persons))
    person_fellow = self.amity.add_person("Tyrion","tyrion@got.world","2345671","F")
    self.assertTrue(person_fellow in self.amity.all_persons)


  def test_adding_staff(self):
    self.assertFalse(check_if_email_used("tyrion@got.world",self.amity.all_persons))
    person_staff =self.amity.add_person("Tyrion","tyrion@got.world","2345671","S")
    #self.assertTrue(person_staff in self.amity.all_persons)

  def test_adding_person_with_invalid_person_type(self):
      self.assertFalse(check_if_email_used("missandei@got.world", self.amity.all_persons))
      sample = self.amity.add_person("Missandei","123456","missandei@got.world","Iii")
      self.assertEqual(sample,-1)
  def test_loading_persons_file(self):
    pass
  def test_allocating_rooms(self):
    pass
  def test_reallocating_rooms(self):
    pass
  def TearDown(self):
    del(self.amity)


def check_if_name_used(name,items):
    for item in items:
      if item.name == name:
        return True
    return False

def check_if_email_used(email,objects):
  for obj in objects:
    if email == obj.email:
      return True
  return False

