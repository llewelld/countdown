# Countdown
Solving the Countdown numbers game

## Summary

Simple code to brute force the Countdown numbers game. The code goes through
every possible formula that can be generated using the integer operators
using the numbers provided, in order to try to calculate a given target
number.

## Inputs

Call the program with a sequence of at least three numbers on the command line.
The last number will be used as the target, all of the numbers up to that
point are for the formula.

This ordering was chosen to match the order the numbers are presented on the
TV show. Makes it easier to enter them while watching the program.

Here's an example from a [classic Coundown game](https://youtu.be/DYW1c41Aw0U?t=10m03s):

```
python countdown.py 6 5 75 25 100 50 814
```
which will eventually generate the output from the show:
```
((((75 + 6) * (50 * 5)) + 100) / 25) = 814
```

## Outputs

The program will output the closest formula it can find to the target number
until it hits the target, at which point it will continue to output all
possible variants.

The approach isn't efficient and many of the formulas will be effectively
duplicates.

## Notes

The Countdown numbers game doesn't require the contestant to use all of the
numbers: if there's a way to get the result with fewer than the full set of
numbers, that's perfectly fine.

To simplify the code, I've used a prune operator in addition to the integer
operators. This ignores the entire branch of a tree on one side of the
operator. Everything that happens in this branch is ignored (not included in
the calculation and not printed out). As a result, some of the formulas
will inevitably be duplicates.

The more efficient way would be to use the standard operators, then run the
program on all subsets of the set of numbers entered. This complicates the code
and adding in the prune operator was easier, so I've gone with this instead,
even though the duplicates are annoying.

## Licence

This code is released under the MIT licence. See the LICENCE file for details.

## Contact

David Llewellyn-Jones

david@flypig.co.uk

