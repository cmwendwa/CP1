import gc
import unittest
from src.amity import Amity
import io


class Tdd_Amity(unittest.TestCase):

    def setUp(self):
        self.amity = Amity()
        self.amity.del_me()
        self.previous_room_count = len(self.amity.all_rooms)

    def test_create_office(self):
        self.assertFalse("Kingslanding" in self.amity.all_rooms.keys())
        self.amity.create_room('Kingslanding', 'O')
        self.assertTrue("Kingslanding" in self.amity.all_rooms.keys())
        new_room_count = len(self.amity.all_rooms)
        self.assertEqual(self.previous_room_count + 1, new_room_count)

    def test_create_office_error_if_exists(self):
        self.assertFalse("Kingslanding" in self.amity.all_rooms.keys())
        self.amity.create_room('Kingslanding', 'O')
        self.assertTrue("Kingslanding" in self.amity.all_rooms.keys())
        response = self.amity.create_room('Kingslanding', 'O')
        self.assertEqual(response, "Room could not be created: Room exists!")

    def test_creating_living_space(self):
        self.assertFalse("Winterfell" in self.amity.all_rooms.keys())
        self.amity.create_room('Winterfell', 'L')
        self.assertTrue("Winterfell" in self.amity.all_rooms.keys())
        # creating an already created room
        try_duplicate = self.amity.create_room('Winterfell', 'L')
        self.assertEqual(
            try_duplicate, "Room could not be created: name taken!")
        new_room_count = len(self.amity.all_rooms)
        self.assertEqual(self.previous_room_count + 1, new_room_count)

    def test_creating_room_with_invalid_room_type(self):
        self.assertTrue("Mereen" not in self.amity.all_rooms.keys())
        sample = self.amity.create_room("Mereen", "K")
        self.assertEqual(sample, -1)

    def test_adding_fellows(self):
        self.assertFalse("tyrion@got.world" in self.amity.all_persons)
        person_fellow = self.amity.add_person(
            "Tyrion", "tyrion@got.world", "FELLOW")
        self.assertTrue(
            "tyrion@got.world" in self.amity.all_persons)
        add_existing = self.amity.add_person(
            "Tyrion", "tyrion@got.world", "FELLOW")

        self.assertEqual(add_existing, "Email already used!")

    def test_adding_staff(self):
        self.assertFalse(
            "tyrion@got.world" in self.amity.all_persons)
        self.amity.add_person("Tyrion", "tyrion@got.world", "STAFF")

        self.assertTrue(
            "tyrion@got.world" in self.amity.all_persons)
        add_existing = self.amity.add_person(
            "Tyrion", "tyrion@got.world", "STAFF")

        self.assertEqual(add_existing, "Email already used!")

    def test_adding_person_with_invalid_person_type(self):
        self.assertFalse("missandei@got.world" in self.amity.all_persons)
        sample = self.amity.add_person(
            "Missandei", "missandei@got.world", "Iii")
        self.assertEqual(sample, -1)

    def test_allocating_rooms(self):
        self.amity.add_person(
            "Tywin", "tywinlannister@got.world", "STAFF")
        r = self.amity.allocate_room("tywinlannister@got.world")

    def test_reallocating_rooms(self):
        self.assertFalse("Kingslanding" in self.amity.all_rooms)
        self.amity.create_room("Kingslanding", "O")
        self.assertTrue("Kingslanding" in self.amity.all_rooms)
        self.amity.create_room("Castle Black", "O")
        self.assertTrue("Castle Black" in self.amity.all_rooms)
        self.amity.add_person(
            "Jaimie Lanister", "jaimie@got.world", "STAFF")
        self.amity.create_room("Casterly", "O")
        self.assertTrue("Casterly" in self.amity.all_rooms)
        self.amity.reallocate_person(
            self.amity.staff["jaimie@got.world"], "Casterly")
        self.assertEqual(self.amity.staff[
                         "jaimie@got.world"].office, "Casterly")

        # reallocating a living space

        self.amity.create_room("Iron Islands", "L")
        self.assertTrue("Iron Islands" in self.amity.all_rooms)
        self.amity.create_room("Mereen", "O")
        self.assertTrue("Mereen" in self.amity.all_rooms)

        self.amity.add_person(
            "Theon Greyjoy", "theon@got.world", "FELLOW", wants_accomodation='Y')
        self.amity.create_room("Winterfell", "L")
        self.assertTrue("Winterfell" in self.amity.all_rooms)
        self.amity.reallocate_person(
            self.amity.fellows["theon@got.world"], "Winterfell")
        self.assertEqual(self.amity.fellows[
                         "theon@got.world"].living_space, "Winterfell")

    def test_amity_edgy_cases(self):
        self.amity.add_person(
            "Theon Greyjoy", "theon@got.world", "FELLOW", wants_accomodation='Y')
        self.amity.create_room("Winterfell", "L")
        self.assertTrue("Winterfell" in self.amity.all_rooms)
        self.amity.reallocate_person(
            self.amity.fellows["theon@got.world"], "Winterfell")
        self.amity.create_room("Mereen", "O")
        self.amity.reallocate_person(
            self.amity.fellows["theon@got.world"], "Mereen")

        self.amity.del_me()
        self.amity.create_room("Winterfell", "O")
        self.amity.add_person(
            "Theon Greyjoy", "theon@got.world", "FELLOW", wants_accomodation='Y')

    def test_loading_persons_file(self):
        self.amity.load_pips_from_text_file(FakeFileWrapper(u"""OLUWAFEMI SULE olu@amity.com FELLOW Y
                                                            DOMINIC WALTERS domi@amity.com STAFF
                                                            SIMON PATTERSON simo@amity.com FELLOW Y
                                                            MARI LAWRENCE mari@amity.com FELLOW Y
                                                            LEIGH RILEY leigh@amity.com STAFF
                                                            LEILA RILEY leila@amity.com STAFF
                                                            TANA LOPEZ tana@amity.com FELLOW Y
                                                            TINA LOPELA tina@amity.com FELLOW N
                                                            KELLY McGUIRE STAFF KELLY McGUIRE STAFF"""))

    def test_get_print_data_methods(self):
        self.assertFalse("Kingslanding" in self.amity.all_rooms)
        self.amity.create_room("Kingslanding", "O")
        self.assertTrue("Kingslanding" in self.amity.all_rooms)
        self.assertFalse("Winterfell" in self.amity.all_rooms)
        self.amity.create_room("Winterfell", "L")
        self.assertTrue("Winterfell" in self.amity.all_rooms)
        self.amity.load_pips_from_text_file(FakeFileWrapper(u"""OLUWAFEMI SULE olu@amity.com FELLOW Y
                                                            DOMINIC WALTERS domi@amity.com STAFF
                                                            SIMON PATTERSON simo@amity.com FELLOW Y
                                                            MARI LAWRENCE mari@amity.com FELLOW Y
                                                            LEIGH RILEY leigh@amity.com STAFF
                                                            LEILA RILEY leila@amity.com STAFF
                                                            TANA LOPEZ tana@amity.com FELLOW Y
                                                            TINA LOPELA tina@amity.com FELLOW N
                                                            KELLY McGUIRE STAFF KELLY McGUIRE STAFF"""))
        data = self.amity.get_print_room_data("Kingslanding")
        self.assertEqual(data['room'], 'Kingslanding')
        self.assertEqual(len(data['names']), 6)

        data2 = self.amity.get_print_allocations_data()
        print(data2)
        self.assertEqual(len(data2['offices']), 1)
        self.assertEqual(len(data2['living']), 1)

        data3 = self.amity.get_print_unallocated_data()
        self.assertNotEqual(data3['living'], None)
        self.assertNotEqual(data3['offices'], None)
        self.amity.load_pips_from_text_file()

    def test_validation_methods(self):
        self.assertEqual(self.amity.validate_db_name("db_mine"), "Valid")
        self.assertEqual(self.amity.validate_db_name("db5"), "Valid")
        self.assertEqual(self.amity.validate_db_name("5db"), "Valid")
        self.assertEqual(self.amity.validate_db_name("db-5"), "Invalid")

        self.assertEqual(self.amity.validate_db_name("&db"), "Invalid")

        self.assertEqual(self.amity.validate_person_name("name"), "Valid")
        self.assertEqual(self.amity.validate_person_name("name1"), "Invalid")
        self.assertEqual(self.amity.validate_person_name("name_"), "Invalid")

        self.assertEqual(self.amity.validate_room_name("valhalla1"), "Valid")
        self.assertEqual(self.amity.validate_room_name("2valhall"), "Invalid")
        self.assertEqual(self.amity.validate_room_name("valhall_1"), "Invalid")

        self.assertEqual(self.amity.validate_room_type("o"), "Valid")
        self.assertEqual(self.amity.validate_room_type("l"), "Valid")
        self.assertEqual(self.amity.validate_room_type("O"), "Valid")
        self.assertEqual(self.amity.validate_room_type("L"), "Valid")
        self.assertEqual(self.amity.validate_room_type("living"), "Invalid")
        self.assertEqual(self.amity.validate_room_type("office"), "Invalid")
        self.assertEqual(self.amity.validate_room_type("jjj"), "Invalid")

        self.assertEqual(self.amity.validate_person_type("Fellow"), "Valid")
        self.assertEqual(self.amity.validate_person_type("staff"), "Valid")
        self.assertEqual(self.amity.validate_person_type("FelloW"), "Valid")
        self.assertEqual(
            self.amity.validate_person_type("anything"), "Invalid")
        self.assertEqual(self.amity.validate_person_type("elow"), "Invalid")
        self.assertEqual(self.amity.validate_person_type("staffk"), "Invalid")
        self.assertEqual(self.amity.validate_person_type("Fellow"), "Valid")

        self.assertEqual(self.amity.validate_email(
            "clementm916@gmail.com"), "Valid")
        self.assertEqual(self.amity.validate_email(
            "1clementm916@gmail.co.ke"), "Valid")
        self.assertEqual(self.amity.validate_email(
            "clementm91_6@gmail.3com"), "Valid")
        self.assertEqual(self.amity.validate_email(
            "clementm-916@gmail"), "Invalid")
        self.assertEqual(self.amity.validate_email(
            "clementm-916gmail.3com"), "Invalid")
        self.assertEqual(self.amity.validate_email(
            "clementm-916@gmail3com"), "Invalid")
        self.assertEqual(self.amity.validate_email(
            "#clementm-916@gmail.3com"), "Invalid")

    def tearDown(self):
        pass


class FakeFileWrapper:
    def __init__(self, text):
        self.text = text

    def open(self):
        return io.StringIO(self.text)
