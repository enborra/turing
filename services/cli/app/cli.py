#!/usr/bin/env python

import subprocess
import click
import os



cli_path = os.path.dirname(os.path.realpath(__file__))
core_sys_path = cli_path + '/commands/'


@click.group()
def cli():
    """Turing client control toolchain."""
    pass

@cli.command()
def start():
    """Boot Turing client processes in background."""

    # click.echo('[TURING.CLI] Starting Turing services...')

    try:
        sys_boot_path = core_sys_path + 'services_start_all.sh'
        bash_cmd = 'sh %s' % sys_boot_path

        output = subprocess.check_output(bash_cmd, shell=True)
        print(output)

    except Exception, e:
        print '[TURING.CLI] ERROR: %s' % str(e)


@cli.command()
def stop():
    """Shut down Turing background processes."""

    # click.echo('[TURING.CLI] Stopping Turing services...')

    try:
        sys_shutdown_path = core_sys_path + 'services_stop_all.sh'
        # bash_cmd = 'python %s/../boot.py' % cli_path

        output = subprocess.check_output(sys_shutdown_path, shell=True)
        print(output)

    except Exception, e:
        print '[TURING.CLI] ERROR: %s' % str(e)

@cli.command()
def update():
    """Update the codebase from origin/master"""

    try:
        sys_boot_path = core_sys_path + 'git_update.sh'
        bash_cmd = 'sh %s' % sys_boot_path

        output = subprocess.check_output(bash_cmd, shell=True)
        print(output)

    except Exception, e:
        print '[TURING.CLI] ERROR: %s' % str(e)



if __name__ == '__main__':
    cli()
