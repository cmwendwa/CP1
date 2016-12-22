#!/usr/bin/env python2.7

"""
Amity Room Allocation System
Usage:
  create_room <room_type> <room_name>
  add_person <first_name> <second_name> <email> <FELLOW|STAFF> [wants_accommodation]
  reallocate_person <email> <new_room_name>
  load_people
  print_allocations [-o=filename] 
  print_unallocated [-o=filename]
  print_room <room_name>
  save_state [--db=sqlite_database] 
  load_state <sqlite_database>
Options:
    -h, --help  Show this screen and exit
"""

import cmd
import shutil
import click
from docopt import docopt, DocoptExit
from src.amity import Amity
from ui_additions import playSpinner

term_size = shutil.get_terminal_size((80, 20))
term_width = term_size[0]


amity = Amity()


def amity_docopt(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """

    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.

            print('Invalid Command!')
            print(e)
            return

        except SystemExit:
            # The SystemExit exception prints help message
            # We do not need to do the print here.
            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn



class AmityInteractive(cmd.Cmd):
    click.secho( "Loading amity ...",fg ='cyan')
    playSpinner()
    click.secho('>' * term_width, fg='cyan', bold=True)
    intro = '\n' \
        + 'Welcome to Amity Room Allocation Application.\n' \
        + 'Add people, create rooms, allocate and reallocate the rooms.\n' \
        + '(type "help" for a list of commands.)\n'
    click.secho(intro, fg="white", bold=True)
    click.secho('>' * term_width, fg='yellow')
    prompt = '(Amity) $ '

    @amity_docopt
    def do_create_room(self, args):
        """
        Creates a room(s) in amity
        Usage:
          create_room <room_type> <room_name> ...
        """
        try:
            room_type = args['<room_type>']
            valid = amity.validate_room_type(room_type)
            if valid == "Invalid":
                error_msg = room_type + " is not a valid room type. \n" + \
                    "Room type can only be 'o' for office or 'l' for livingspace; case insensitive."
                click.secho(error_msg, fg='red')
                return
            count = 0
            for name in args['<room_name>']:
                if amity.validate_room_name(name) == "Invalid":
                    click.secho(
                        name + " is not a valid room name, change it and try again!!", fg='red')
                    break
                room = amity.create_room(name, room_type.upper())
                if room == "Room could not be created: Room exists!":
                    click.secho(room, fg='red')
            if not count == 0:
                msg = str(count) + "room(s) successfully added"
                click.secho(msg, fg='green')
        except:
            click.secho("An unexpected error occured while running the comand",fg='red')

    @amity_docopt
    def do_add_person(self, args):
        """
        Add a person to amity.
        Usage:
          add_person <first_name> <second_name> <email> <person_type> [--accommodation=N]
        """
        try:
            first_valid = amity.validate_person_name(args['<first_name>'])
            if first_valid == "Invalid":
                error_msg = args[
                    '<first_name>'] + " is not a valid name, a person's name can only contain letters!!"
                click.secho(error_msg, fg='red')
                return
            second_valid = amity.validate_person_name(args['<second_name>'])
            if second_valid == "Invalid":
                error_msg = args[
                    '<second_name>'] + " is not a valid name, a person's name can only contain letters!!"
                click.secho(error_msg, fg='red')
                return
            name = ' '.join([args['<first_name>'], args['<second_name>']])
            if amity.validate_email(args['<email>']) == "Invalid":
                error_msg = args['<email>'] + " is not a valid email."
                click.secho(error_msg, fg='red')

            email = args['<email>']
            if amity.validate_person_type(args['<person_type>']) == "Invalid":
                error_msg = args[
                    '<person_type>'] + " is not valid person type.\n Person type can be either 'staff' or 'fellow'; case insensitive."
                click.secho(error_msg, fg='red')

            person_type = args['<person_type>']
            if args['--accommodation'] == None:
                args['--accommodation'] == 'N'
            if args['--accommodation']:
                if amity.validate_wants_accommodation(args['--accommodation']) == "Invalid":
                    error_msg = "Accommodation can either be 'Y' for yes or 'N' for no"
                    click.secho(error_msg,fg='red')
                    return
                wants_accommodation = args['--accommodation']
            else: 
                wants_accommodation = 'N'
            

            new_person = amity.add_person(
                name, email, person_type.upper(), wants_accommodation.upper())

            if new_person == "Email already used!":
                click.secho(
                    "Could not add a new person. Provided email already taken!!", fg='red')
                return
            elif new_person == -1:
                click.secho("Unfortunately, could not add a new person", fg='red')
            else:
                click.secho(name + " added successfully to amity", fg='green')
        except:
            click.secho("An unexpected error occured while running the comand",fg='red')

    @amity_docopt
    def do_reallocate_person(self, args):
        """
        Reallocate peron to another room.
        Usage:
          reallocate_person <email> <new_room>
        """
        try:
            if amity.validate_email(args['<email>']) == "Invalid":
                error_msg = args['<email>'] + " is not a valid email."
                click.secho(error_msg, fg='red')
                return
            if amity.validate_room_name(args['<room_name>']) == "Invalid":
                click.secho(
                    name + " is not a valid room name, change and try again!!", fg='red')

            email = args['<email>']
            new_room = args['<new_room>']
            if not email in amity.all_persons:
                click.secho(email + " not in the system!!", fg='red')
            else:
                if amity.all_persons[email].person_type == "Fellow":
                    person = amity.fellows[email]
                    if person.office == new_room or person.living_space == new_room:
                        click.secho(
                            "Been here all along,kindly let be!", fg='cyan')
                        return
                elif amity.all_persons[email].person_type == "Staff":
                    person = amity.staff[email]
                    if person.office == new_room:
                        click.secho("Been here all along,kindly le be", fg='cyan')
                        return
                else:
                    click.secho("An alien type discovered!!", fg='red')
                    return

            amity.reallocate_person(args['<email>'], args['<new_room>'])

        except:
            click.secho("An unexpected error occured while running the comand",fg='red')

    @amity_docopt
    def do_load_people(self, args):
        """
        Loads people from a text file.
        usage:
            load_people
         """
        try:

            status = amity.load_pips_from_text_file()


            if not status == -1:
                playSpinner()
                click.secho("People loaded successfully!!", fg='green')
        except:
            click.secho("An unexpected error occured while running the comand",fg='red')

    @amity_docopt
    def do_print_allocations(self, args):
        """
        Prints a list of unallocated people to the screen. 
        Specifying the -o option here outputs the information to the txt file provided
        usage:
            print_allocations [--o=filename] 

        """
        try:

            if not args['--o']:
                data = amity.get_print_allocations_data()
                offices = data['offices']
                living = data['living']


                
                click.secho("OFFICES",fg='cyan',bold=True)
                for office in offices:

                    click.secho(office['room'].capitalize(), fg='green', bold=True)
                    for name in office['names']:
                        click.secho(name, fg='white')

               
                click.secho("LIVING SPACES")
                for room in living:
                    click.secho(room['room'].capitalize(), fg='green', bold=True)
                    for name in room['names']:
                        click.secho(name, fg='white')




            elif args['--o']:

                print('Args:' + str(args['--o']))
                if amity.validate_db_name(args['--o'])=="Invalid":
                    click.secho("Provided name is not an acceptable file name.",fg='red')
                    return
                state = amity.get_print_allocations_data(args['--o'])

        except:
            click.secho("An unexpected error occured while running the comand",fg='red')


    @amity_docopt
    def do_print_unallocated(self, args):
        """
        Prints a list of unallocated people to the screen. 
        Specifying the -o option here outputs the information to the txt file provided
        usage:
            print_unallocated [--o=filename]
        """
        try:

            if not args['--o']:
                data = amity.get_print_unallocated_data()
                if not data == -1:
                    offices = data['offices']
                    living = data['living']
                    click.secho("Unallocated to offices\n")
                    click.secho("Name\t\t id\t\t Email\t")

                    for person in offices:
                        click.secho(person[0]+"\t"+person[1]+"\t"+person[2])

                    click.secho("\n\nUnallocated to living spaces")
                    click.secho("\nName\t\t id\t\t Email\t",fg='blue')
                    for person in living:
                        click.secho(person[0]+"\t"+person[1]+"\t"+person[2])
                else:
                    click.secho("Ooopsie!! No data to print.",fg='cyan')

            elif args['--o']:
                if amity.validate_db_name(args['--o']) == "Invalid":
                    click.secho("Provided name is not an acceptable file name.",fg='red')
                    return
                    
                amity.get_print_unallocated_data(args['--o'])
        except:
            click.secho("An unexpected error occured while running the comand",fg='red')
        

    @amity_docopt
    def do_print_room(self, args):
        """
        Prints  the names of all the people in room_name on the screen.

        usage:
            print_room <room_name>
        """
        try:
            data = amity.get_print_room_data(args['<room_name>'])

            click.secho(data['room'].upper(), fg='green', bold=True)
            click.secho(
                "x"*term_width, fg='yellow')
            for name in data['names']:
                click.secho(name, fg='blue')

        except KeyError:
            click.secho("The room you tried to print does not exist", fg='red')

    @amity_docopt
    def do_save_state(self, args):
        """Persists all the data stored in the app to a SQLite database. 
           Specifying the --db parameter explicitly stores the data in the sqlite_database specified.
           usage:
            save_state [--db=sqlite_database]
        """
        try:
            if args['--db']:

                if amity.validate_db_name(args['--db'])== "Valid":
                    amity.save_state_to_db(args['--db'])
                    playSpinner()
                    click.secho("State saved successfully to database",fg='green')
                else:
                    click.secho("Provide a valid database name",fg='red')
                    return
            else:
                amity.save_state_to_db()
                playSpinner()
                click.secho("State saved successfully to database",fg='green')
        except:
            click.secho("An unexpected error occured while running the comand",fg='red')


    @amity_docopt
    def do_load_state(self, args):
        """
        Loads data from a database into the application.
        usage:
            load_state <sqlite_database>

        """
        try:
            if args['<sqlite_database>']:
                if amity.validate_db_name(args['<sqlite_database>']) == "Valid":
                    
                    playSpinner()
                    state=amity.load_state_from_db(args['<sqlite_database>'])
                    if not state == -1:
                        click.secho("State loaded successfully from data",fg='green')
                else:
                    click.secho("Provide a valid database name",fg='red')
                    return

        except:
            click.secho("An unexpected error occured while running the comand",fg='red')



    @amity_docopt
    def do_quit(self, args):
        """
        Type to leave the app.
        usage:
            quit
        """
        click.sech("Thank you and see you again. BYEBYE!",fg='cyan')
        exit()

if __name__ == '__main__':
    try:
        
        AmityInteractive().cmdloop()

    except:
        pass

