from abc import ABCMeta, abstractmethod


class Room(object):
    """

    Abstract basec class for room objects.

    """
    __meta__ = ABCMeta

    def __init__(self, name):
        self.name = name
        self.allocated_spaces = 0
        self.unallocated_spaces = self.capacity - self.allocated_spaces

    @property
    def _is_full(self):
        """
        True when capacity equals allocation, false otherwise.

        """
        if self.allocated_spaces == self.capacity:
            return True
        elif self.allocated_spaces < self.capacity:
            return False

    @property
    def _is_empty(self):
        """
        True when there are no allcations to the room.

        """
        if self.allocated_spaces == 0:
            return True
        else:
            return False

    def allocate_room_space(self):
        """
        Records the allocation of a room to a person

        """
        if self._is_full == True:
            return -1
        else:
            self.allocated_spaces += 1

            self.unallocated_spaces = self.capacity - self.allocated_spaces
            return "Room Allocated"

    def deallocate_room_space(self):
        """
        Records the deallocation of a person from a room.

        """
        if self._is_empty:
            return - 1
        else:
            self.allocated_spaces = self.allocated_spaces - 1
            self.unallocated_spaces = self.capacity - self.allocated_spaces


class LivingSpace(Room):
    """
    Creates rooms for living in.

    """
    capacity = 4

    def __init__(self, room_name):
        self.room_type ="LivingSpace"
        super(LivingSpace, self).__init__(room_name)

    


class Office(Room):
    """
    Creates office rooms.

    """
    capacity = 6

    def __init__(self, room_name):
        self.room_type = "OfficeSpace"
        super(Office, self).__init__(room_name,)

