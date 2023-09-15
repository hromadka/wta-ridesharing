# Poisson point process

import numpy as np

def poisson_process(lmbda, max_time):
    """
    Simulate a Poisson process with a given lambda rate for a specified duration.

    Args:
    - lmbda: Poisson rate (average number of events per unit time).
    - max_time: Duration of the simulation in seconds.

    Yields:
    - Timestamp of each event occurrence.
    """
    t = 0
    event_times = []
    while t < max_time:
        # Generate a random time until the next event using exponential distribution
        next_event_time = np.random.exponential(1 / lmbda)
        event_times.append(next_event_time)

        # user timer ticks to calculate all events, not a walltime real sleep timer

        # Update the current time
        t += next_event_time
        
        # Yield the timestamp of the event
        yield t


lmbda = 1.0  # Poisson rate (events per second)
max_time = 10  # Duration of the simulation in seconds

print("Simulating a Poisson process with lambda =", lmbda)
for event_time in poisson_process(lmbda, max_time):
    print(f"Event at time {event_time:.2f} seconds")
