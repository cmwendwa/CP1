from abc import ABCMeta, abstractmethod
class Person(object):
  __metaclass__ =ABCMeta
  def __init__(self,name,phone,email):
    self.name = name
    self.phone =phone
    self.email = email
    
  @abstractmethod
  def person_type(self):
        """"Return a string representing the type of person this is(staff | fellow)."""

  def __del__(self):
    return None
class Staff(Person):
  def __init__(self,name,phone,email):
    super(Staff, self).__init__(name,phone,email)
  @property
  def person_type(self):
        """"Return a string representing the type of person this is(staff | fellow)."""
        return "Staff"
class Fellow(Person):
  def __init__(self,name,phone,email):
    super(Fellow, self).__init__(name,phone,email)
  
  @property
  def person_type(self):
        """"Return a string representing the type of person this is(staff | fellow)."""
        return "Fellow"





