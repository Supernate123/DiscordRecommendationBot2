# guess the number
import random
import surprise
from pkg_resources import get_distribution
number = random.randint(1, 10)
max_tries = 3
guess = 0
for counter in range(max_tries):
  guess = int(input("Guess the number: "))
  print(f"in loop, you tried {counter+1} times")
  if guess == number:
    print("You are correct!")
    break
  else:
    print("You are wrong ! Try again !")
print("The number was", number)
print("out of the loop")