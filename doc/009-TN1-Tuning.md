# Tuning Mode

In tuning mode we attempt to tune a limited set of component choices, possibly only one.

## TN1 - Introduce Tune mode

Action - Add a mode query function to simulations and species 
Action - After normal species execution, run the tuning species
Action - Add tuning maker that just copies the best member and specializes it
Action - Have random maker and top choices maker switch off during tuning
Action - Report mode in report

## TN1 - Include prototype at start of tune

Action - Base all introduced members on the prototype member. A clone of the configuration would suffice.