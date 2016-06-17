# Puzzles

## Ya

Checking execution time with `timeit`

$ python3 -m timeit -n 100 "import menu; menu.generate_menu(365)"
100 loops, best of 3: 25.8 msec per loop

$ python3 -m timeit -n 100 "import menu; menu.generate_menu2(365)"
100 loops, best of 3: 12.3 msec per loop
