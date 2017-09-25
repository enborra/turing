# THE TURING SYSTEM

## A DROID, WITH SERVICES

Turing operates as a Droid, which can be custom built or downloaded, and the
Turing Services the Droid lists as dependencies. These services may range
from data storage, to facial recognition, to motor control adapters.

The Droid is the soul of the system, though. The Droid gives the system it's
character, its decision-making around response to environmental input.

All Turing Services act as behaviors - additional nervous-system inputs or
outputs that govern some skill. All Turing Services run as singletons, assuming
the same service cannot be initiated more than once simultaneously.

## BASIC SYSTEM OPERATION

Turing runs on a single-droid-per-system arrangement - assuming the single Droid
codebase in operation has full control over the system faculties - speakers, mic,
databases, network, whatever the various Turing services (which also function as
singleton services on ports) require.

## THE TURING CLI

Basic control of system booting and shutdown happens through the CLI currently.
The CLI has versions built for both macOS, and Raspberry Pi.

## CORE SERVICES

All Turing Droids and Services depend on a number of core Services that come
out of the box with the core Turing codebase.

Full Core Services documentation at /docs/CoreServices.md
