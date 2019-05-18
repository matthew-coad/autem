# Autem Standard Models

The autem standard model defines how we extend autem with new features.

## Core

The core model is base structure that autem applications sit on. They are the host for autem state data and most components work in conjunction with them.
The current core classes are:

+ Simulation - The core simulation object.
+ Specie - A specie which owns a independant optimization effort
+ Epoch - A substantial portion of the simulation. Composed in sequence in epochs.
+ Member - A single member that tests one possible solution.

## Settings 

Settings are defined hierachically. Defining a setting at the simulation defines it for all objects. Settings are considered public.

## State

State is considered an internal implementation detail. Typically not available out of the namespace. They also strictly belong to a container.

## Queries

Queries are high level objects that integrate data from the model. They compose high level facts from the model, settings and state. Queries are public
across autem and are expected to be utilized by other components. They are not used to change state.

They may operate across the model hierachy or be specific to a given level.
