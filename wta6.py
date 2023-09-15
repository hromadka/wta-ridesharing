import sys
import datetime
import random
import time
import numpy as np
from itertools import combinations
from itertools import permutations

print("GREETINGS PROFESSOR FALKEN.")

starttime = time.time()

problem_type = 1

range_low = 100
range_high = 500

dt = 3
MAX_SIM_TIME = 400

poisson_lambda = 1.0
poisson_max_time = 200  # generally: 2x num_targets

def poisson_process(lmbda, max_time):
    t = 0
    event_times = []
    while t < max_time:
        # Generate a random time until the next event using exponential distribution
        next_event_time = np.random.exponential(1 / lmbda)
        event_times.append(t)
        t += next_event_time
    return event_times



class weapon:
    def __init__(self, id, type, range):
            self.id = id
            self.type = type
            self.range = range

class target:
     def __init__(self, id, type, distance, value):
            self.id = id
            self.type = type
            self.distance = distance
            self.value = value

current_timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
filename = f"{current_timestamp}.txt"
f = open(filename, 'a')
f.write('dt, poisson_lambda, poisson_max_time, problem_type\n')
params = [dt, poisson_lambda, poisson_max_time, problem_type]
header = (','.join(str(p) for p in params))
f.write('{}\n'.format(header)) 

MAX_NUM_SIMS = 1000
for simcount in range(1,MAX_NUM_SIMS):
    print(simcount)
 
#    f.write('weapon,target,score\n')

    #match problem_type:  # not yet -- py 3.10
    if (problem_type == 1):
    #    case 1:
        # MC problem
        num_weapons = 100    # set
        num_weapon_types = 3
        weapon_inventory = []
        for i in range(0,num_weapons):
            weapon_inventory.append(weapon(i, random.randint(0, num_weapon_types-1),random.randint(range_low,range_high)))

        num_targets = num_weapons
        num_target_types = 3
        target_list = []
        for j in range(0,num_targets):
            target_list.append(target(j, random.randint(0,num_target_types-1),random.randint(range_low,range_high),random.randint(1,num_targets)))   # interesting: let target value = 0 for targets to ignore?

        #psurvivals = np.ones((num_weapon_types,num_target_types)) * random.random()  
        psurvivals = np.ones((num_weapon_types,num_target_types)) * 0.7  
    #    case 2:
    elif (problem_type == 2):
        # Wiki problem = https://en.wikipedia.org/wiki/Weapon_target_assignment_problem
        # solution uses powersets
        weapon_inventory = []
        weapon_inventory.append(weapon(0,0,100))
        weapon_inventory.append(weapon(1,0,100))
        weapon_inventory.append(weapon(2,0,100))
        weapon_inventory.append(weapon(3,0,100))
        weapon_inventory.append(weapon(4,0,100))
        weapon_inventory.append(weapon(5,1,100))
        weapon_inventory.append(weapon(6,1,100))
        weapon_inventory.append(weapon(7,2,100))
        num_weapons = len(weapon_inventory) # get
        num_weapon_types = 3
        target_list = []
        target_list.append(target(0,0,100,5))
        target_list.append(target(1,1,100,10))
        target_list.append(target(2,2,100,20))
        num_targets = len(target_list)
        num_target_types = 3
        pkills = np.array([[0.3,0.2,0.5],[0.1,0.6,0.5],[0.4,0.5,0.4]])
        psurvivals = np.ones((3,3)) - pkills    
    #    case _:
    else:
        print("unknown problem type selected.")
        weapon_inventory = []
        target_list = []
        psurvivals = []

    #print('--- weapons ---')
    #print(weapon_inventory[0].id)
    #print(weapon_inventory[0].type)
    #print(weapon_inventory[0].range)
    #print(num_weapons)
    #print('--- targets ---')
    #print(target_list[1].id)
    #print(target_list[1].type)
    #print(target_list[1].distance)
    #print(target_list[1].value)
    #print(num_targets)
    #print('--- psurvival ---')
    #print(psurvivals)     





    event_times = poisson_process(poisson_lambda, poisson_max_time*2)  # important: pass a float for the lambda value
    #print(event_times)
    #print(len(event_times))
    if (len(event_times) < num_targets):
        print("error!  too few target events simulated.")
        sys.exit()



    tick = 0                # simulation time
    last_dt = 0             # closing time of previous window
    active_targets = []     # dispatch queue for this window
    weapons_remaining = weapon_inventory.copy()
    running_score = 0.0
    while tick < MAX_SIM_TIME:
        tick += 1
        if (tick == (dt+last_dt)):
            before = len([i for i in event_times if i < last_dt])
            current = len([i for i in event_times if i < dt+last_dt])
            #print("tick ",tick,"count ",c, "event_times[-1] ",event_times[c-1], "event_times[0] ",event_times[c], "event_times[+1]", event_times[c+1])
    #        print(tick, dt, before, current, current-before)    # note: we generated more target events than there are targets

            for e in range(before,current):
                if (e > num_targets-1):
                    tick = MAX_SIM_TIME+1  # exit simulation after this iteration
                    print("no targets remaining")
                    break
    #            print("adding target.id ",target_list[e].id)
                active_targets.append(target_list[e])   # populate dispatch queue

            
            # process these targets as a standalone SWTA scenario
            # greedy algo = pick highest value target, assign best single remaining weapon for that target
            # brute force = try every permutation, pick the best assignment
            # other heuristics etc
    #        print('--------------------')
            for t in active_targets:
                best_weapon = weapons_remaining[0]
                for w in weapons_remaining:     # could use set(weapons.type) to eliminate duplicates
    #                print(t.id, t.type, t.value, w.id, w.type, psurvivals[w.type][t.type])
                    if (psurvivals[w.type][t.type] < psurvivals[best_weapon.type][t.type]):
                        best_weapon = w
                    weighted_score_this_target = psurvivals[best_weapon.type][t.type]*t.value
                print("assign ", best_weapon.id, " to target ", t.id, ", score = ", weighted_score_this_target)
                nums = [best_weapon.id, t.id, weighted_score_this_target]
                tmp = (','.join(str(n) for n in nums))
#                f.write('{}\n'.format(tmp))                     
                running_score += weighted_score_this_target
                weapons_remaining.remove(best_weapon)
    #            print(len(weapons_remaining))
                if (len(weapons_remaining) <= 0):
                    tick = MAX_SIM_TIME+1  # exit simulation after this iteration
                    print("weapon inventory exhausted")
                    break
            # process weapon/target effectiveness, remove destroyed targets (only) from active_targets list
            # note: this is comparable to DWTA shoot-look-shoot scenario


            #for e in event_times:
                # range last_dt to dt+last_dt
            last_dt += dt

    print("solution score = ", running_score)
    f.write('solution score = {}\n'.format(running_score))
    simcount += 1

f.close()
print('done')

endtime = time.time()
print("runtime = ", endtime-starttime)