import random
import matplotlib.pyplot as plt

from stocks.write_file import write_to_file

#https://williamsinstitute.law.ucla.edu/publications/adult-lgbt-pop-us/

#pictures/gayness.png

NAME = 'GAY'

gayness_perstate = {
    "Alabama": 4.6,
    "Alaska": 5.9,
    "Arizona": 5.9,
    "Arkansas": 5.3,
    "California": 5.1,
    "Colorado": 6.8,
    "Connecticut": 6.0,
    "Delaware": 7.5,
    "Florida": 5.4,
    "Georgia": 5.1,
    "Hawaii": 5.1,
    "Idaho": 5.3,
    "Illinois": 4.5,
    "Indiana": 5.4,
    "Iowa": 4.7,
    "Kansas": 5.9,
    "Kentucky": 4.9,
    "Louisiana": 5.7,
    "Maine": 6.8,
    "Maryland": 5.4,
    "Massachusetts": 6.5,
    "Michigan": 6.0,
    "Minnesota": 6.3,
    "Mississippi": 4.1,
    "Missouri": 6.0,
    "Montana": 5.1,
    "Nebraska": 5.5,
    "Nevada": 6.6,
    "New Hampshire": 7.2,
    "New Jersey": 5.3,
    "New Mexico": 5.5,
    "New York": 5.5,
    "North Carolina": 4.4,
    "North Dakota": 4.9,
    "Ohio": 6.2,
    "Oklahoma": 5.5,
    "Oregon": 7.8,
    "Pennsylvania": 5.8,
    "Rhode Island": 6.5,
    "South Carolina": 4.9,
    "South Dakota": 5.3,
    "Tennessee": 6.3,
    "Texas": 5.1,
    "Utah": 6.1,
    "Vermont": 7.1,
    "Virginia": 5.9,
    "Washington": 6.9,
    "West Virginia": 4.1,
    "Wisconsin": 5.7,
    "Wyoming": 5.9
    }


def get_gayness():
    state = random.choice(list(gayness_perstate.keys()))
    value = gayness_perstate[state]
    write_to_file(NAME, value)
    return value

if __name__ == "__main__":
    values = []

    for i in range(100):
        state = random.choice(list(gayness_perstate.keys()))

    stock_gay = gayness_perstate[state]
    values.append(stock_gay)

    #write some code to diaply a line graph of values

    plt.plot(values)
    plt.ylabel('Gayness')
    plt.show()
