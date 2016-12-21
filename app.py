#!/usr/bin/env python2.7

"""
Amity Room Allocation System
Usage:
  create_room (l|o) <room_name>
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

import sys
import cmd
import click
from docopt import docopt, DocoptExit
from src.amity import Amity


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
            # The SystemExit exception prints the usage for --help
            # We do not need to do the print here.

            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn


def start():
    arguments = __doc__
    print(arguments)


class AmityInteractive(cmd.Cmd):
    intro = '>>>>*****************************************************<<<<\n' \
        + 'Welcome to Amity Room Allocation Application.\n' \
        + 'Add people, create rooms, allocate and reallocate the rooms.\n' \
        + '(type help for a list of commands.)\n'\
        + '>>>>*****************************************************<<<<'
    prompt = '(Amity) $'

    @amity_docopt
    def do_create_room(self, args):
        """
        Creates a room(s) in amity
        Usage:
          create_room (o|l) <room_name> ...
        """
        # try:
        for name in args['<room_name>']:
            amity.create_room(name, args['<room_type>'])

        # except:
        #     pass

    @amity_docopt
    def do_add_person(self, args):
        """
        Add a person to amity.
        Usage:
          add_person <first_name> <second_name> <email> (fellow|staff) [wants_accommodation]
        """
        try:
            pass

        except:
            pass

        print ("Adding person")

    @amity_docopt
    def do_reallocate_person(self, args):
        """
        Reallocate peron to another room.
        Usage:
          reallocate_person <email> <new_room>
        """

        #try:
        amity.reallocate_person(args['<email>'], args['<new_room>'])

        # except:
        #     pass

        print("Allocating rooms")

    @amity_docopt
    def do_load_people(self, args):
        """
        Loads people from a text file.
        usage:
            load_people

        """
        # try:
        amity.load_pips_from_text_file()
        # except:
        #     pass
        # finally:
        #     print("Loading people")

    @amity_docopt
    def do_print_allocations(self, args):
        """
        Prints a list of unallocated people to the screen. 
        Specifying the -o option here outputs the information to the txt file provided
        usage:
            print_allocations [-o=filename] 
        
        """
        data = amity.get_print_allocations_data()
        offices = data['offices']
        living =  data['living']

        office_info = """"""
        click.secho("OFFICES")
        for office in offices:

            click.secho(office['room'].capitalize(),fg='green',bold=True)
            for name in office['names']:
                click.secho(name,fg='white')

        living_info =""""""
        click.secho("LIVING SPACES")
        for room in living:
            click.secho(room['room'].capitalize(),fg='green',bold=True)
            for name in room['names']:
                click.secho(name,fg='white')

    @amity_docopt
    def do_print_unallocated(self, args):
        """
        Prints a list of unallocated people to the screen. 
        Specifying the -o option here outputs the information to the txt file provided
        usage:
            print_unallocated [-o=filename]
        """
        data = amity.get_print_unallocated_data()
        offices = data['offices']
        living =  data['living']

        office_info = """"""
        for office in offices:
            click.secho(office['room'].capitalize(),fg='green',bold=True)
            for name in office['names']:
                click.secho(name,fg='white')

        living_info =""""""
        for room in living:
            click.secho(room['room'].capitalize(),fg='green',bold=True)
            for name in room['names']:
                click.secho(name,fg='white')
    

    @amity_docopt
    def do_print_room(self, args):
        """
        Prints  the names of all the people in room_name on the screen.

        usage:
            print_room <room_name>
        """
        # try:
        data = amity.get_print_room_data(args['<room_name>'])
        
        click.secho(data['room'].upper(),fg='green',bold=True)
        click.secho("+++++++++++++++++++++++++++++++++++++++++++++++++",fg='yellow')
        for name in data['names']:
            click.secho(name,fg='blue')


        # except:
        #     pass
        # finally:
        #     click.secho("Printing room")

    @amity_docopt
    def do_save_state(self, args):
        """Persists all the data stored in the app to a SQLite database. 
           Specifying the --db parameter explicitly stores the data in the sqlite_database specified.
           usage:
            save_state [--db=sqlite_database]
        """
        amity.save_state_to_db(args['sqlite_database'])

    @amity_docopt
    def do_load_state(self, args):
        """
        Loads data from a database into the application.
        usage:
            load_state <sqlite_database>

        """

        amity.load_state_from_db(args['<sqlite_database>'])


        print("Loading status")

    @amity_docopt
    def do_quit(self, args):
        exit()

    def organize_data(self,data):
        data = amity.get_print_unallocated_data()
        offices = data['offices']
        living =  data['living']

        office_info = """"""

        living_info =""""""

        print(data)
    


# opt = docopt(__doc__, sys.argv[1:])

# if opt['--interactive']:

if __name__ == '__main__':
    start()
    AmityInteractive().cmdloop()

def validate_email(email):
    if not re.match(r"[^A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$",email):
        return "Valid"
    else:
        return "Invalid"

