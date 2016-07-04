import sys
import traceback

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



try:
    output_msg('Starting up.')

except KeyboardInterrupt:
    output_msg('Shutting down.')
