import os  # when working with read/write file modification

# get the correct index
index = lambda x, y: x + 5 * y
Color = index
Nation = index
Pet = index
Drink = index
Cigar = index

ranges = [(0, 4, Color), (5, 9, Nation), (10, 14, Pet), (15, 19, Drink), (20, 24, Cigar)]

# Colors
Red = 0
Green = 1
White = 2
Yellow = 3
Blue = 4

# Nationalities
Brit = 5
Swede = 6
Dane = 7
German = 8
Norwegian = 9

# Pets
Dog = 10
Horse = 11
Cat = 12
Bird = 13
Fish = 14

# Drinks
Water = 15
Milk = 16
Beer = 17
Tea = 18
Coffee = 19

# Cigarettes
Pall_Mall = 20
Bluemasters = 21
Prince = 22
Blends = 23
Dunhill = 24


def all_questions():
    question = []
    numerically = []
    for i in range(1, 6):
        for c in ['Red', 'Green', 'White', 'Yellow', 'Blue']:
            question.append('{:5.0f}: Is Color of House {} {}?'.format(Color(i, eval(c)), i, c))
        for n in ['Brit', 'Swede', 'Dane', 'German', 'Norwegian']:
            question.append('{:5.0f}: Is Nationality of House {} {}?'.format(Nation(i, eval(n)), i, n))
        for p in ['Dog', 'Horse', 'Cat', 'Bird', 'Fish']:
            question.append('{:5.0f}: Is Pet of House {} {}?'.format(Pet(i, eval(p)), i, p))
        for d in ['Water', 'Milk', 'Beer', 'Tea', 'Coffee']:
            question.append('{:5.0f}: Is Drink of House {} {}?'.format(Drink(i, eval(d)), i, d))
        for c in ['Pall_Mall', 'Bluemasters', 'Prince', 'Blends', 'Dunhill']:
            question.append('{:5.0f}: Is Cigar of House {} {}?'.format(Cigar(i, eval(c)), i, c))
        numerically = sorted(question)

    return os.linesep.join(numerically)


def base_cases(i, j, cat):
    line = []
    for i in range(i, j + 1):  # want end to be inclusive
        houses = []  # each house has a value for each category
        for h in range(1, 6):  # at least one statement in every 5 questions must be true
            houses.append(str(cat(h, i)))
        houses.append('0')
        line.append(' '.join(houses))

        for house_1 in range(1, 6):
            # not same value of category for different houses, no 2 houses can be red
            for house_2 in range(1, house_1):
                line.append('-{} -{} {}'.format(cat(house_1, i), cat(house_2, i), '0'))
            for j in range(i, j + 1):  # not more than 1 value of a category per house
                if i != j:
                    line.append('-{} -{} {}'.format(cat(house_1, i), cat(house_1, j), '0'))
    return os.linesep.join(line)


def pairs(cat1, val1, cat2, val2):
    line = []
    for i in range(1, 6):  # p -> q translates to p V -q, do it both ways (-p q, p -q)
        line.append('-{} {} {}'.format(cat1(i, val1), cat2(i, val2), '0'))
        line.append('{} -{} {}'.format(cat1(i, val1), cat2(i, val2), '0'))
    return os.linesep.join(line)


def neighbors(cat1, val1, cat2, val2):
    line = []
    line.append('-{} {} {}'.format(cat1(1, val1), cat2(2, val2), '0'))  # if first house, neighbor must be 2nd house
    line.append('-{} {} {}'.format(cat1(5, val1), cat2(4, val2), '0'))  # if last (5th) house, neighbor 4th house

    for i in range(2, 5):  # if middle houses, neighbor can be both left or right
        line.append('-{} {} {} {}'.format(cat1(i, val1), cat2(i-1, val2), cat2(i+1, val2), '0'))
    return os.linesep.join(line)


def problem_line(line):
    var = set()
    lines = line.split(os.linesep)
    for line in lines:  # number of different numbers (ignoring sign) = # of variables
        vals = line.split(' ')
        for v in vals:
            var.add(abs(int(v)))
    return 'p cnf {} {}'.format(len(var)-1, len(lines))


def einstein_puzzle_hints():
    constraints = []
    for r in ranges:
        constraints.append(base_cases(r[0], r[1], r[2]))

    constraints.append(pairs(Nation, Brit, Color, Red))  # The Brit lives in the red house.
    constraints.append(pairs(Nation, Swede, Pet, Dog))  # The Swede keeps dogs as Pets.
    constraints.append(pairs(Nation, Dane, Drink, Tea))  # The Dane drinks tea.
    constraints.append(pairs(Color, Green, Drink, Coffee))  # The green house’s owner drinks coffee.
    constraints.append(pairs(Cigar, Pall_Mall, Pet, Bird))  # The person who smokes Pall Mall rears birds.
    constraints.append(pairs(Color, Yellow, Cigar, Dunhill))  # The owner of the yellow house smokes Dunhill.
    constraints.append(pairs(Cigar, Bluemasters, Drink, Beer))  # The owner who smokes Bluemasters drinks beer.
    constraints.append(pairs(Nation, German, Cigar, Prince))  # The German smokes Prince.

    # The man who smokes Blends lives next to the one who keeps cats.
    constraints.append(neighbors(Cigar, Blends, Pet, Cat))
    # The man who keeps the horse lives next to the man who smokes Dunhill.
    constraints.append(neighbors(Pet, Horse, Cigar, Dunhill))
    # The man who smokes Blends has a neighbor who drinks water
    constraints.append(neighbors(Cigar, Blends, Drink, Water))

    constraints.append('{} {}'.format(Drink(3, Milk), '0'))  # The man living in center house drinks milk.
    constraints.append('{} {}'.format(Nation(1, Norwegian), '0'))  # The Norwegian lives in the first house.
    constraints.append('{} {}'.format(Color(2, Blue), '0'))  # The Norwegian lives next to the blue house.

    # The green house is on the left of the white house.
    for i in range(1, 6):  # white
        for j in range(1, 6):  # green
            if j != i-1 and j != i:  # same house condition already checked and i-1 indicates green is left of white
                constraints.append('-{} -{} {}'.format(Color(i, White), Color(j, Green), '0'))
    final = os.linesep.join(constraints)
    formula = os.linesep.join(["c CNF Encoding of Einstein's Puzzle", os.linesep.join([problem_line(final), final])])
    return formula


if __name__ == '__main__':
    with open('input.cnf', 'w') as file:
        inputs = einstein_puzzle_hints()
        file.write(inputs)
    with open('questions.txt', 'w') as file:
        file.write(all_questions())

