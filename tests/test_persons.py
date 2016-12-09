import unittest
from ..src.person import Person,Staff, Fellow


class TddPersons(unittest.TestCase):
  def setUp(self):
    self.fellow = None
    self.staff = None
    
  def test_instantiating_a_fellow(self):
    self.fellow = Fellow("Tyrion","123456","tyrion@got.world.com")
    self.assertIsInstance(self.fellow,Person) 

  def test_instantiating_a_staff(self): 
    self.staff = Staff("Tyrion","123456","tyrion@got.world.com")
    self.assertIsInstance(self.staff,Person)
    self.assertEqual(self.staff.person_type, "Staff")

  
  def test_instantiating_three_persons_then_check_identifiers(self):
    pass


  def TearDown(self):
    del(self.fellow)
    del(self.staff)