import unittest
from src.person import Person, Staff, Fellow


class TddPersons(unittest.TestCase):
    def setUp(self):
        self.staff = Staff("Tyrion", "Tyrion@got.world.com")
        self.fellow = Fellow("Missandei", "missandei@got.world.com")
        self.fellow2 = Fellow("arya", "arya@got.world.com", "Y")

    def test_instantiating_a_fellow(self):
        self.assertIsInstance(self.fellow, Person)
        self.assertEqual(self.fellow.wants_accomodation, 'N')
        self.assertEqual(self.fellow.person_type, "Fellow")

    def test_instantiating_a_staff(self):
        self.assertIsInstance(self.staff, Person)
        self.assertEqual(self.staff.person_type, "Staff")

    def test_setting_offices(self):
        unset_offices = (self.fellow.office, self.staff.office)
        self.assertEqual(unset_offices, (None, None))
        self.fellow.set_office("Mereen")
        self.staff.set_office("Kingslanding")
        set_offices = (self.fellow.office, self.staff.office)
        self.assertEqual(set_offices, ("Mereen", "Kingslanding"))
        
    def test_fellow_accomodation(self):
        self.assertEqual(self.fellow.wants_accomodation, "N")
        self.assertEqual(self.fellow2.wants_accomodation, "Y")
        self.assertEqual(self.fellow.living_space, None)
        self.assertEqual(self.fellow2.living_space, None)
        fellow = self.fellow.set_livingspace("Dothraki")
        self.fellow2.set_livingspace("Winterfell")
        self.assertEqual((fellow, self.fellow2.living_space),
                         (-1, "Winterfell"))
        

    def TearDown(self):
        del self.fellow
        del self.staff
