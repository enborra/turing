#!/usr/bin/env python3

import subprocess
import click
import os

from core import CommandService


cli_path = os.path.dirname(os.path.realpath(__file__))
core_sys_path = cli_path + '/commands/'

mgr = CommandService()


@click.group()
def cli():
    """Turing client control toolchain."""
    pass

@cli.command()
def start():
    """Boot Turing client processes in background."""

    mgr.start_all_services()


@cli.command()
def stop():
    """Shut down Turing background processes."""

    mgr.stop_all_services()

@cli.command()
def update():
    """Update the codebase from origin/master"""

    mgr._services_update_source()

@cli.command()
def install():
    """Update the codebase from origin/master"""

    mgr.install_all_services()


@cli.command()
def status():
    """Get status of all running local Turing services"""

    mgr.get_system_status()


def _run_bash_script(file_path):
    try:
        sys_boot_path = core_sys_path + file_path
        bash_cmd = 'sh %s' % sys_boot_path

        output = subprocess.check_output(bash_cmd, shell=True)
        print(output)

    except Exception as e:
        click.echo('[TURING.CLI] Error: %s' % str(e))






if __name__ == '__main__':
    print()
    cli()
