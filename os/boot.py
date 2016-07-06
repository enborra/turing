import sys
import traceback

from core import Client



def global_excepthook(*args):
    print >> sys.stderr, '[TURING.OS] Caught global excepthook.'
    print >> sys.stderr, args

    traceback.print_tb(err.__traceback__)

sys.excepthook = global_excepthook


#
# Set up and initialize Turing OS
#

def output_msg(msg):
    print "[TURING.OS] %s" % msg





c = Client()

try:
    output_msg('Starting up.')

    c.start()


except KeyboardInterrupt:
    output_msg('Shutting down.')

    try:
        sys.stdout.close()
    except:
        pass

    try:
        sys.stderr.close()
    except:
        pass

    c.stop()
    c.destroy()
