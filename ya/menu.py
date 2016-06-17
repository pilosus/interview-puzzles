#!/usr/bin/env python3

import random
import bisect
import itertools
import sys

### Constants
MAINS = {'chicken': 0.3, 'beef': 0.3, 'fish': 0.25, 'pork': 0.15}
STAPLES = {'rice': 0.2, 'buckwheat': 0.15, 'pasta': 0.04,
           'potato': 0.01, 'vegs': 0.6}
SNACKS = {'bread': 0.1, 'cheese': 0.15, 'mayonnese': 0.03, 'none': 0.72}

PLATE =  """
                      ___         
         ||||     .-"`   `"-.     / |  __
    |||| ||||   .'  .-'`'-.  '.   | | /  \\
    |||| \  /  /  .'       '.  \  | | ;();
    \  /  ||  /  ;           ;  \  \| \  /
     ||   ||  | ;             ; |  ||  ||
     %%   %%  | ;             ; |  %%  %%
     %%   %%  \  ;           ;  /  %%  %%
     %%   %%   \  '.       .'  /   %%  %%
     %%   %%    '.  `-.,.-'  .'    %%  %%
     %%   %%      '-.,___,.-'      %%  %%

     ======= PLAT DU JOUR, OLA-LA! ======
             Main course: {0}
             Side dish: {1}
             Snacks: {2}
"""

class Menu(object):
    """Menu consists of a main course, side dish and a snack."""

    def __init__(self, main, staple, snack):
        self.main = main
        self.staple = staple
        self.snack = snack

    def is_digestable(self):
        """Return True if all dishes satisfy certain compatibility rules.
        """
        return not ((self.main == 'fish' and self.staple == 'pasta')
                    or (self.staple == 'pasta' and self.snack == 'bread')
                    or (self.main == 'pork' and self.staple == 'potato'
                        and self.snack != 'none'))

    def __repr__(self):
        return """{0} | {1} | {2}""".format(self.main, self.staple, self.snack)

    def __str__(self):
        """Representation of Menu object when printing it.

        print(Menu('fish', 'potato', 'none'))
        """
        return PLATE.format(self.main, self.staple, self.snack)

def random_pick(weighted_choices: (str, int)) -> str:
    """Choose value randomly taking weights into account.
    """
    choices, weights = zip(*weighted_choices)
    cumdist = list(itertools.accumulate(weights))
    x = random.random() * cumdist[-1]
    return choices[bisect.bisect(cumdist, x)]
    
def generate_menu(days: int) -> [Menu]:
    """Return list of Menu for number of days specified.

    days >= 2
    """
    mains = list(map(lambda n: (n, round(MAINS[n] * days)), MAINS))
    staples = list(map(lambda n: (n, round(STAPLES[n] * days)), STAPLES))
    snacks = list(map(lambda n: (n, round(SNACKS[n] * days)), SNACKS))

    menu_list = []

    while(days):
        menu = Menu(random_pick(mains), random_pick(staples),
                    random_pick(snacks))
        if menu.is_digestable():
            menu_list.append(menu)
            days -=1

    return menu_list

def distribution(weighted_choices: (str, int)) -> [str]:
    return [val for val, cnt in weighted_choices for i in range(cnt)]
    
def generate_menu2(days: int) -> [Menu]:
    """Return list of Menu for number of days specified.

    Faster implementation, as distribution lists get generated once.

    days >= 2
    """
    menu_list = []

    mains = distribution(map(lambda n: (n, round(MAINS[n] * days)), MAINS))
    staples = distribution(map(lambda n: (n, round(STAPLES[n] * days)), STAPLES))
    snacks = distribution(map(lambda n: (n, round(SNACKS[n] * days)), SNACKS))

    while(days):
        menu = Menu(random.choice(mains), random.choice(staples),
                    random.choice(snacks))
        if menu.is_digestable():
            menu_list.append(menu)
            days -=1

    return menu_list

if __name__ == '__main__':
    args = sys.argv[1:]
    try:
        days = int(args[0])
    except:
        days = 365
    menu = generate_menu2(days)
    for e, i in enumerate(menu):
        print("     ============ Day {0} Menu =============".format(e + 1))
        print(i)
