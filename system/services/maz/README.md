# CORE SERVICE: `MAZ`

Web interface for droid operation

## HOW IT WORKS

Maz is a Python server based on the Flask HTTP framework that exposes various
UI configuration and instrumentation through a web interface.

It communicates across the common `CENTRALSTATION` core service, which serves
as an MQTT-based communications pipeline.
