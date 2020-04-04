# Prime ASCII Generator

The scripts `ascii.py` and `prime.py` work together to find
primes that look like a given image.

## 1. Make an ascii template with `ascii.py`

The script `ascii.py` converts an image into in an ascii image
using digits. As such, `ascii.py` maps an image to a number.

Place an image in the `images` and run `python ascii.py`.
Specify the name of an image and the maximum number of
digits the prime ascii should have. The more digits, the
better the ascii image will look. Note that the more digits
the longer it takes to determine if a number is prime.

## 2. Scatter spaces into the template

Scatter spaces into the resulting image of `ascii.py` by manually
replacing unimportant digits with an empty space character ` `.

Spaces are treated as variable digits by `prime.py`. The
more spaces you scatter, the more numbers `primes.py` can
check. Pick parts of the image that would work as any digit.
The edges of objects tend to be good choices.

Be sure that the digit in the bottom right corner is not
even or divisible by 5! Otherwise, it is impossible to find
a prime that matches the tempate!

## 3. Find primes that match the template with `prime.py`

This script checks every number that matches the given
template. Variable digits (space characters) are replaced
with every possible combination of digits.

This script can take a very long time to run; however, you can
monitor it's results by looking at the `tmp/work-x` files.
As the script runs, lines are printed to these files. Each
line corresponds to a found prime.

The script can be multithreaded to utilize more CPU cores.

## Example results

```
7777777777777777777777777777777777777777777777
7777777777777777770000000000077777777777777777
7777777777777777000777777777000777777777777777
7777777777777700077700000007770077777777777777
7777777777777700770007777700077007777777777777
7777777777777007700077000770007700777777777777
7777777777777007700770070077007700777777777777
7777777777777007770077770077007700777777777777
7777777777777700777000000770007700777777777777
7777777777777770007777777700077007777777777777
7777777777777777700000000007770077777777777777
7777777777770777777770007777000777777777777777
7777770000000000000777777000077777777777777777
7777000077777777770000000007770000000000077777
7770077700000000077700770077000777777770007777
7700770000777770000770000770007700000007700077
7007700077700007700077000770077007777000770077
7007700770027200770077000770077007007770077007
7007700770000770077007700770077002700770077007
7007740077777700777007700770007770007700575007
7700777000750000770077770077000077777000770077
7770067770000977700777777007777000000077700777
7777000077777700007777777700007777777770007777
7777777000000007777777777777000000000000777777
7777777777777777777777777777777777777777777777
```
