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

Here's an example from a [classic Countdown game](https://youtu.be/DYW1c41Aw0U?t=10m03s):

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

### Binary tree enumeration

The key to the overall approach is in the `shuntconnection()` function.
Repeated application of this function can be used to enumerate all possible
binary trees containing the given number of leaf nodes.

Every formula can be represented as a tree, where parent nodes are operators
and leaf nodes are numbers, so each tree ends up being a formula to check.

### Duplicates

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

### Naive approach

A naive approach to solving these things would be to simply permute all of the
numbers and operators, then apply the operators to the numbers in order.
Code to do this can be seen in the `naive.py` file. However, this doesn't
cover all possibilities. Take the simple example of numbers 1, 1, 2 and 4, in
an attempt to reach a target of 15. If you just apply operators in order you
never reach a solution. To get the right result, you have to use brackets,
for example (1 + 2) * (1 + 4) = 15. Without the brackets it can't be done,
and the naive version will claim it to be impossible.

## Licence

This code is released under the MIT licence. See the LICENCE file for details.

## Contact

David Llewellyn-Jones

david@flypig.co.uk

