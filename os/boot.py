import sys
import traceback

from core import Client
from core import Settings



def global_excepthook(*args):
    print >> sys.stderr, '[TURING.OS] Caught global excepthook.'
    print >> sys.stderr, args

    traceback.print_tb(err.__traceback__)

sys.excepthook = global_excepthook


#
# Set up and initialize Turing OS
#

def output_msg(msg):
    print "[TURING] %s" % msg


output_msg('Booting')

c = Client()

try:
    c.start()


except KeyboardInterrupt:
    output_msg('Shutting down.')

    c.stop()

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
