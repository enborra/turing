# TURING CORE SERVICES

Core Services are located in the main Turing directory path,
under `/system/services`

All core services are required for basic operation of any bot - they are
interdependent and cannot be selectively included or removed.

Addon services, however, are built as separate feature functionality and
core services take no hard dependencies on addon services. Add-on Services are
hosted on the local system under the data directory, at `/etc/turing`

## `MAZ`: WEB INTERFACE FOR DROID CONTROL

Maz serves as a hard-dependency of all Turing Droids, providing a visual
interface

## `CENTRALSTATION`: THE PRIMARY COMMUNICATIONS HUB

CentralStation services as the central nervous sytem for a droid, as an in-system,
technology agnostic MQTT-pipeline any service can communicate with other
services across.

## `CLI`: THE COMMAND-LINE INTERFACE FOR HUMANS INTERACTING WITH THE OS

The CLI service powers the command-line interaction with the core operating
system.
