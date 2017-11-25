# THE TURING SYSTEM

## A droid, with services.

Turing operates as a Droid, which can be custom built or downloaded, and the
Turing Services the Droid lists as dependencies. These services may range
from data storage, to facial recognition, to motor control adapters.

The Droid is the soul of the system, though. The Droid gives the system it's
character, its decision-making around response to environmental input.

All Turing Services act as behaviors - additional nervous-system inputs or
outputs that govern some skill. All Turing Services run as singletons, assuming
the same service cannot be initiated more than once simultaneously.

## HOW IT WORKS

### Building and Running a Droid.
Building a droid starts with with building the configuration required to run
any droid. The Turing OS codebase is kept physically separate from the code that
runs your droid, allowing source control of the droid itself.

#### Turing Framework
Turing framework lives at: ~/projects/turing

Turing expects a config file to exist at /private/etc/turing/config.json, which
details which Droid should be loaded, and the local file paths to available
droids, and available Turing services.

Droid code lives at `/etc/turing`


## SYSTEM OPERATION

Turing runs on a single-droid-per-system arrangement - assuming the single Droid
codebase in operation has full control over the system faculties - speakers, mic,
databases, network, whatever the various Turing services (which also function as
singleton services on ports) require.

### Core services.
All Turing Droids and Services depend on a number of core Services that come
out of the box with the core Turing codebase.

Full Core Services documentation at `/system/services/README.md`

### The Turing CLI.
Basic control of system booting and shutdown happens through the CLI currently.
The CLI has versions built for both macOS, and Raspberry Pi. This functionality
runs from the `CLI` core service, located at `/system/services/cli`.
