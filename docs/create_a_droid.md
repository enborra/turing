# How to Create a New Turing Droid

## a. Create a directory for your droid

## b. Symlink your droid repo into /etc/turing/droids

To keep concerns serparated between the Turing framework/execution and your custom
code, any droids or services you build are symlink'd in to the Turing directory.

This lets you maintain separate source control on your projects, and keep
your Turing install up to date as updates and fixes are published.

  sudo ln -s "/path/to/your/repo" "/etc/turing/droids/{{your_named_droid}}"

## b. Create a service.json in that directory

Turing expects a service.json file that details the execution plan
for the droid, and what other Turing service dependencies it will have.

## c. Define a boot path in service.json

(TODO: looks like Turing doesn't even bother, currently. Should probably
wire this up.)

  {
    "run": "boot.sh"
  }

## d. Create a boot.sh

(TODO: not confident Turing bothers here either, at the moment.)

## e. Create a /app directory

(TODO: this is just for hygiene, not functionally needed at all at the moment)

## f. Create a boot script in the language of your choice

(TODO: boot.py, boot.js, whatever, that boot.sh knows how to call.)
