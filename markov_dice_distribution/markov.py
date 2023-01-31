import numpy
import sys

#Sum of dice distribution

#10d6
#NO_DICE_ROLL = 10
#NO_DIE_FACE = 6

if len(sys.argv) < 3:
    print('Not enough parameter! Usage: markov.py <no_dice_roll> <no_die_face>')
    sys.exit(-1)

NO_DICE_ROLL = int(sys.argv[1])
NO_DIE_FACE = int(sys.argv[2])

NO_OF_STATES = NO_DICE_ROLL*NO_DIE_FACE + 1
list_of_prob = [1/NO_DIE_FACE for i in range(NO_DIE_FACE)]

trans = numpy.zeros((NO_OF_STATES, NO_OF_STATES))
input_vec = numpy.zeros((1, NO_OF_STATES))
input_vec[0][0] = 1

count = 1
for row in trans:
    for i in range(len(list_of_prob)):
        if count + i < NO_OF_STATES:
            row[count + i] = list_of_prob[i]
    count += 1

final_trans = trans.copy()
for i in range(NO_DICE_ROLL - 1):
    final_trans = numpy.matmul(final_trans, trans)

output_vec = numpy.matmul(input_vec, final_trans)

print("Probability distribution of {}d{} being:".format(NO_DICE_ROLL, NO_DIE_FACE))
state = 0
total = 0
for elem in output_vec[0]:
    if state >= NO_DICE_ROLL:
        print('{}\t:\t{:.6f}%'.format(state, elem*100))
    state += 1
    total += elem

print("Total sum of probability: {}%".format(total*100))


        
