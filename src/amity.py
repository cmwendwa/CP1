import os
import re
from random import randint
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from .room import Office, LivingSpace
from .person import Fellow, Staff
from .db_organisation.db_logic import DbManager, Base, Rooms, Persons


class Amity(object):
    """
    Amity class implementing the logic of a facility where it has rooms which can be offices or living spaces. An office can occupy a maximum of 6 people. A living space can inhabit a maximum of 4 people
    A person to be allocated could be a fellow or staff. Staff cannot be allocated living spaces. Fellows have a choice to choose a living space or not.

    """

    offices = {}
    living_spaces = {}
    fellows = {}
    staff = {}

    def create_room(self, name, typ):
        if typ == "O":
            if not name in self.all_rooms.keys():
                new_room = Office(name)
                self.offices[name] = {'room': new_room, "occupants": []}

                return "Room created succesfully"
            else:
                return "Room could not be created: Room exists!"

        elif typ == "L":
            if not name in self.all_rooms.keys():
                new_room = LivingSpace(name)
                self.living_spaces[name] = {'room': new_room, "occupants": []}

                return "Room created succesfully"
            else:
                return "Room could not be created: name taken!"

        else:
            return -1

    def add_person(self, name, email, typ, wants_accomodation='N'):
        if typ == "FELLOW":
            if not email in self.all_persons.keys():
                new_fellow = Fellow(name, email, wants_accomodation)
                self.fellows[email] = new_fellow
                self.allocate_room(new_fellow)
                return new_fellow
            else:
                return "Email already used!"
        elif typ == "STAFF":
            if not email in self.all_persons.keys():
                new_staff = Staff(name, email)
                self.staff[email] = new_staff
                self.allocate_room(new_staff)
                return new_staff
            else:
                return "Email already used!"
        else:
            return -1

    def allocate_room(self, person):
        if self.unallocated_spaces[0] == 0:
            return "No office space available"
        self.random_assign(person, self.offices)

        if person.person_type == "Fellow":
            if person.wants_accomodation == "Y":
                if self.unallocated_spaces[1] == 0:
                    return "No room space available"
                else:
                    self.random_assign(person, self.living_spaces)

    def reallocate_person(self, person, new_room):
        room_type = self.all_rooms[new_room]['room'].room_type
        if room_type == "OfficeSpace":
            if person.office == None:
                return "Could not reallocate"
            else:
                self.deallocate_person(person, room_type)
                self.assign_room(person, new_room)

                return "Reallocated"
        elif room_type == "LivingSpace":
            if person.living_space == None:
                return "Could not reallocate"
            else:
                self.deallocate_person(person, room_type)
                self.assign_room(person, new_room)

                return "Reallocated"

    def deallocate_person(self, person, room_type):
        if room_type == "OfficeSpace":
            room = person.office
            self.offices[room]['room'].deallocate_room_space()
            self.offices[room]['occupants'].remove(person.name)
            person.set_office(None)
        elif room_type == "LivingSpace":
            room = person.living_space
            self.living_spaces[room]['room'].deallocate_room_space()
            self.living_spaces[room]['occupants'].remove(person.name)
            person.set_livingspace(None)

    def assign_room(self, person, room):
        if self.all_rooms[room]['room'].room_type == "OfficeSpace":
            person.set_office(room)
            self.offices[room]['room'].allocate_room_space()
            self.offices[room]['occupants'].append(person.name)

        elif self.all_rooms[room]['room'].room_type == "LivingSpace":
            if not person.set_livingspace(self.living_spaces[room]['room'].name) == -1:
                self.living_spaces[room]['room'].allocate_room_space()
                self.living_spaces[room]['occupants'].append(person.name)

    def remove_room(self):  # pragma: no cover
        pass  # pragma: no cover

    def remove_person(self):  # pragma: no cover
        pass  # pragma: no cover

    @property
    def all_rooms(self):
        all_rooms = {}
        all_rooms.update(self.offices)
        all_rooms.update(self.living_spaces)
        return all_rooms

    @property
    def all_persons(self):
        all_persons = {}
        all_persons.update(self.staff)
        all_persons.update(self.fellows)
        return all_persons

    @property
    def unallocated_spaces(self):
        unallocated_offices = 0
        for office in self.offices:
            unallocated_offices += self.offices[
                office]['room'].unallocated_spaces
        unallocated_living = 0
        for living in self.living_spaces:
            unallocated_living += self.living_spaces[
                living]['room'].unallocated_spaces

        return [unallocated_offices, unallocated_living]

    def random_select(self, room_set):
        set_size = len(room_set)
        set_keys = list(room_set.keys())
        random_key = set_keys[randint(0, set_size - 1)]
        return random_key

    def random_assign(self, person, room_set):
        random_room = self.random_select(room_set)
        while room_set[random_room]['room'].allocate_room_space() == -1:
            random_room = self.random_select(room_set)  # pragma: no cover
        if self.all_rooms[random_room]['room'].room_type == "LivingSpace":
            person.set_livingspace(
                self.living_spaces[random_room]['room'].name)
            room_set[random_room]['occupants'].append(person.name)
        elif self.all_rooms[random_room]['room'].room_type == "OfficeSpace":
            person.set_office(self.offices[random_room]['room'].name)
            room_set[random_room]['occupants'].append(person.name)

    def load_pips_from_text_file(self, file_access=None):
        people = []
        if file_access == None:
            filename = "sample.txt"
            file_access = FileAccessWrapper(filename)

        with file_access.open() as sf:
            lines = sf.readlines()
            for item in lines:
                people.append(item.split())
        for person in people:
            if len(person) == 4:
                #re.sub(' +', ' ', person)
                self.add_person(name=str(' '.join(person[:2])), email=person[
                                2], typ=person[3])
            elif len(person) == 5:
                self.add_person(name=str(' '.join(person[:2])), email=person[
                                2], typ=person[3], wants_accomodation=person[4])

    def get_print_room_data(self, room):
        habitants = self.all_rooms[room]['occupants']

        return {'room': room, 'names': habitants}

    def get_print_allocations_data(self, file=None):
        living_spaces = []
        offices = []
        for room in self.living_spaces.keys():
            room_data = self.get_print_room_data(
                self.living_spaces[room]['room'].name)
            living_spaces.append(room_data)

        for room in self.offices.keys():
            room_data = self.get_print_room_data(
                self.offices[room]['room'].name)
            offices.append(room_data)

        return {'offices': offices, 'living': living_spaces}

    def get_print_unallocated_data(self, file=None):
        unallocated_to_office = []
        for person in self.all_persons.keys():
            if self.all_persons[person].office == None:
                name = self.all_persons[person].name
                identifier = self.all_persons[person].person_id
                email = self.all_persons[person].email

                unallocated_to_office.append([name, identifier, email])

        unallocated_to_living = []
        for person in self.fellows.keys():
            if self.fellows[person].wants_accomodation == 'N':
                continue
            elif self.fellows[person].wants_accomodation == 'Y':
                if self.fellows[person].living_space == None:
                    name = self.fellows[person].name
                    identifier = self.fellows[person].person_id
                    email = self.fellows[person].email
                    unallocated_to_living.append([name, identifier, email])
        return {'offices': unallocated_to_office, "living": unallocated_to_living}

    def save_state_to_db(self, db_name=None):
        if db_name == None:
            amity_db = DbManager()
        else:
            amity_db = DbManager(db_name)

        Base.metadata.bind = db.engine
        amity_session = amity_db.session()

        for person in self.all_persons:
            if self.all_persons[person].person_type == "FELLOW":
                wants_accomodation = person.wants_accomodation
            elif self.all_persons[person].person_type == "STAFF":
                wants_accomodation = None

            person_db = Persons(person_id=self.all_persons[person].person_id,
                                email=self.all_persons[person.email],
                                name=self.all_persons[person].name,
                                wants_accomodation=wants_accomodation,
                                allocated_living=self.all_persons[
                                    person].living_space,
                                allocated_office=self.all_persons[
                                    person].office,
                                person_type=self.all_persons[person].person_type)

            amity_session.merge(person_db)

        for room in self.all_rooms:
            room_db = Rooms(name=self.all_rooms[room]['room'].name,
                            room_type=self.all_rooms[room]['room'])
            amity_session.merge(room_db)

            amity_session.commit()

    def load_state_from_db(self, db_name):
        if not os.path.exists('sqlite:///' + db_name + '.sqlite'):
            return
        self.del_me()
        engine = create_engine('sqlite:///' + db_name + '.sqlite')
        Session = sessionmaker()
        Session.configure(bind=engine)
        session = Session()
        all_people = session.query(People).all()
        all_rooms = session.query(Rooms).all()

        for room in all_rooms:
            self.create_room(room.name, room.room_type)

        for person in all_people:
            self.add_person(person.name, person.email,
                            person.person_type, person.wants_accomodation)
            self.all_persons[person.email].person_id = person.person_id

            if person.person_type == "Staff":
                self.reallocate_person(person.email, person.allocated_office)
            elif person.person_type == "Fellow":
                self.reallocate_person(person.email, person.allocated_office)

                if person.wants_accomodation == "Y":
                    self.reallocate_person(
                        person.email, person.allocated_living)

    def validate_room_name(self, word):
        matches = re.match(r'^[A-Za-z][A-Za-z0-9]*$', word, re.IGNORECASE)
        if matches:
            return "Valid"
        else:
            return "Invalid"

    def validate_person_name(self, word):
        matches = re.match(r'^[A-Za-z]+$', word, re.IGNORECASE)
        if matches:
            return "Valid"
        else:
            return "Invalid"

    def validate_db_name(self,word):
        matches = re.match(r'^[a-zA-Z0-9]([a-zA-Z0-9_])*[a-zA-Z0-9]$', word, re.IGNORECASE)
        if matches:
            return "Valid"
        else:
            return "Invalid"

    def validate_person_type(self,word):
        matches = re.match(r'^staff$|^fellow$', word, re.IGNORECASE)
        
        if matches:
            return "Valid"
        else:
            return "Invalid"

    def validate_room_type(self,word):
        matches = re.match(r'^o$|^l$', word, re.IGNORECASE)
        if matches:
            return "Valid"
        else:
            return "Invalid"

    def del_me(self):
        self.offices = {}
        self.living_spaces = {}
        self.fellows = {}
        self.staff = {}


class FileAccessWrapper:
    def __init__(self, filenname):
        self.filenname = filenname

    def open(self):
        return open(self.filenname, "r")
