# Amity Application
Amity is a console application that's used for room allocations. With this application you create rooms and add people who will be randomly assigned to the rooms. There are two types of rooms: offices and living spaces. There are two types of people in amity: staff and fellows. A fellow has the option to get a living room while a staff can only be allocated to an office. This comes with other capabilities as enlisted below.


# Installation
Todo app is a python package and can be installed as such. First setup a virtual environment where the application's dependencies will be automatically installed:
```sh
$ pip install virtualenv          #install virtualenv module
$ virtualenv amity-app                #setup your own virtual env
$ source amity-app/bin/activate #to activate environment in linux, in windows run amit-app/scripts/activate
```
To install the app, clone this repository: 
```sh
$ https://github.com/clementm916/CP1.git
$ cd CP1
$ $ pip install -r requirements.txt         #ensure your environments are activated
#this installs all required modules
```

# Setting Up
Todo was developed with Python version `3.5`  but works properly with python 2.7. To run the application in   using the following command:
```sh
$ python app.py
Loading amity ...
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

Welcome to Amity Room Allocation Application.
Add people, create rooms, allocate and reallocate the rooms.
(type "help" for a list of commands.)

>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

Welcome to Amity Room Allocation Application.
Add people, create rooms, allocate and reallocate the rooms.
(type "help" for a list of commands.)

```

# Functionality

### `help` command
Returns all commands
```sh
(Amity) $ help

Documented commands (type help <topic>):
========================================
add_person   load_people        print_room         reallocate_person
create_room  load_state         print_unallocated  save_state
help         print_allocations  quit                        
```sh     
### `--help` option
This is to help the user whenever they have trouble using a given command:
```sh
(Amity) $ add_person --help
        Add a person to amity.
        Usage:
          add_person <first_name> <second_name> <email> <person_type> [--accommodation=N]
```

### `create_room` command
Creates a new room in the amity system. Can take several rooms at a go.
```sh
(Amity) $ create_room --help
        Creates a room(s) in amity
        Usage:
          create_room <room_type> <room_name> ...
```


### `add_person` command
Adds a new person to the amity system.
```sh
(Amity) $ add_person --help
        Add a person to amity.
        Usage:
          add_person <first_name> <second_name> <email> <person_type> [--accommodation=N]
```

### `reallocate_person` command
Reallocates a person to a different room.
```sh
(Amity) $ reallocate_person --help
        Reallocate peron to another room.
        Usage:
          reallocate_person <email> <new_room>

```

### `load_people` command
Loads people from a text file.
```sh
(Amity) $ load_people --help
        Loads people from a text file.
        usage:
            load_people
```
### `print_unallocated` command
Prints the people in Amity who have not been allocated to rooms. Takes an optional file argument printing them to the file otherwise prints to screen.
```sh
(Amity) $ print_unallocated --help
        Prints a list of unallocated people to the screen.
        Specifying the -o option here outputs the information to the txt file provided
        usage:
            print_unallocated [--o=filename]
```
### `print_allocations` command
Prints the rooms and the members in them.
```sh
(Amity) $ print_allocations --help
        Prints a list of unallocated people to the screen.
        Specifying the -o option here outputs the information to the txt file provided
        usage:
            print_allocations [--o=filename]

```

### `save_state` command
Saves state of the application to a persistent database. Takes an optional database name.
```sh
(Amity) $ save_state --help
Persists all the data stored in the app to a SQLite database.
           Specifying the --db parameter explicitly stores the data in the sqlite_database specified.
           usage:
            save_state [--db=sqlite_database]
```
### `load_state` command
Loads saved state from persistent database. The name must be passed.
```sh
(Amity) $ load_state --help
        Loads data from a database into the application.
        usage:
            load_state <sqlite_database>
```


