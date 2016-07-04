#!/usr/bin/env python

import subprocess
import click
import os



cli_path = os.path.dirname(os.path.realpath(__file__))
core_sys_path = cli_path + '/../../system/'


@click.group()
def cli():
    """Turing client control toolchain."""
    pass

@cli.command()
def start():
    """Boot Turing client processes in background."""

    click.echo('[TURING.CLI] Requesting boot...')

    try:
        sys_boot_path = core_sys_path + 'run/turing_boot.sh'
        bash_cmd = 'python %s/../boot.py' % cli_path

        output = subprocess.check_output(bash_cmd, shell=True)
        print(output)

    except Exception, e:
        print '[TURING.CLI] ERROR: %s' % str(e)


@cli.command()
def stop():
    """Shut down Turing background processes."""

    click.echo('[TURING.CLI] Requesting shutdown...')

    try:
        sys_shutdown_path = core_sys_path + 'run/turing_stop.sh'
        # bash_cmd = 'python %s/../boot.py' % cli_path

        output = subprocess.check_output(sys_shutdown_path, shell=True)
        print(output)

    except Exception, e:
        print '[TURING.CLI] ERROR: %s' % str(e)



if __name__ == '__main__':
    cli()
