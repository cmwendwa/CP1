import unittest
from src.room import Room, Office, LivingSpace


class TddRooms(unittest.TestCase):
    def setUp(self):
        self.office = Office("Kingslanding")
        self.living_space = LivingSpace("Winterfel")

    def test_room_type_for_office(self):
        typ = self.office.room_type
        self.assertEqual(typ, "OfficeSpace")
        self.assertIsInstance(self.living_space, Room)

    def test_room_type_for_living_space(self):
        typ = self.living_space.room_type
        self.assertEqual(typ, "LivingSpace")
        self.assertIsInstance(self.living_space, Room)

    def test_allocating_one_occupant_to_office(self):
        self.office.allocate_room_space()
        allocated = self.office.allocated_spaces
        unallocated = self.office.unallocated_spaces
        self.assertEqual(allocated, 1)
        self.assertEqual(unallocated, 5)

    def test_allocating_one_occupant_to_living_space(self):
        self.living_space.allocate_room_space()
        allocated = self.living_space.allocated_spaces
        unallocated = self.living_space.unallocated_spaces
        self.assertEqual(allocated, 1)
        self.assertEqual(unallocated, 3)

    def test_allocating_a_valid_number_of_occupants_to_office(self):
        for i in range(4):
            self.office.allocate_room_space()
        allocated = self.office.allocated_spaces
        unallocated = self.office.unallocated_spaces
        self.assertEqual(allocated, 4)
        self.assertEqual(unallocated, 2)

    def test_deallocating_an_empty_room(self):
      dealloc = self.office.deallocate_room_space()
      self.assertEqual(dealloc,-1)

    def test_adding_permitted_number_of_occupants_to_living_space(self):
        for i in range(3):
            self.living_space.allocate_room_space()
        allocated = self.living_space.allocated_spaces
        unallocated = self.living_space.unallocated_spaces
        self.assertEqual(allocated, 3)
        self.assertEqual(unallocated, 1)

    def test_adding_excess_number_of_occupants_to_office(self):
        for i in range(6):
            self.office.allocate_room_space()
        allocated = self.office.allocated_spaces
        unallocated = self.office.unallocated_spaces
        self.assertEqual(allocated, 6)
        self.assertEqual(unallocated, 0)

        assign_excess = self.office.allocate_room_space()
        self.assertEqual(assign_excess, -1)

    def test_adding_excess_number_of_occupants_to_living_space(self):
        for i in range(4):
            self.living_space.allocate_room_space()
        allocated = self.living_space.allocated_spaces
        unallocated = self.living_space.unallocated_spaces
        self.assertEqual(allocated, 4)
        self.assertEqual(unallocated, 0)
        assign_excess = self.living_space.allocate_room_space()
