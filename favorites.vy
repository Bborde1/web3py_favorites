# pragma version 0.4.0
# @license MIT

has_favorite_number: bool
my_favorite_number: public(uint256)
my_address: address

struct Person:
    favorite_number: uint256
    name: String[100]

list_of_numbers: public(uint256[5])
list_of_people: public(Person[5])
name_to_favorite_number: public(HashMap[String[100], uint256])
index: public(uint256)

struct Car:
    year: uint256
    color: String[100]

list_of_cars: public(Car[10])

##################################################
#Reference data types
# - Fixed size list
nums: public(uint256[10])
# - Mapping
myMap: public(HashMap[address, uint256])
# - Structs
# struct Person:
#     favorite_number: uint256
#     name: String[100]
# - Dynamic arrays

# @pure - do not read any state and global variables
# @view - read state and global variables
###################################################

@deploy
def __init__():
    self.my_favorite_number = 90

@external
def store(new_number: uint256):
    self.my_favorite_number = new_number

@external
@view
def retrieve() -> uint256:
    return self.my_favorite_number

@external
def add_person(name: String[100], favorite_number: uint256):
    #Add Number to list
    self.list_of_numbers[self.index] = favorite_number
    #Add struct to list
    new_person: Person = Person(favorite_number = favorite_number, name=name)
    self.list_of_people[self.index] = new_person

    #Add person and favorite number to hash map
    self.name_to_favorite_number[name] = favorite_number
    self.index += 1

@external
def add_one_to_favorite_number():
    self.my_favorite_number = self.my_favorite_number + 1

@external
def create_car(year: uint256, color: String[100]):
    new_car: Car = Car(year = year, color = color)
    self.list_of_cars[self.index] = new_car