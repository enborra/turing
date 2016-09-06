#!/usr/bin/env python

import subprocess
import click
import os

from core import CommandService


cli_path = os.path.dirname(os.path.realpath(__file__))
core_sys_path = cli_path + '/commands/'


@click.group()
def cli():
    """Turing client control toolchain."""
    pass

@cli.command()
def start():
    """Boot Turing client processes in background."""

    CommandService.run_script('services_start_all.sh')


@cli.command()
def stop():
    """Shut down Turing background processes."""

    CommandService.run_script('services_stop_all.sh')

@cli.command()
def update():
    """Update the codebase from origin/master"""

    CommandService.run_script('git_update.sh')


@cli.command()
def status():
    """Get status of all running local Turing services"""

    CommandService.get_system_status()


def _run_bash_script(file_path):
    try:
        sys_boot_path = core_sys_path + file_path
        bash_cmd = 'sh %s' % sys_boot_path

        output = subprocess.check_output(bash_cmd, shell=True)
        print(output)

    except Exception, e:
        click.echo('[TURING.CLI] Error: %s' % str(e))






if __name__ == '__main__':
    cli()
