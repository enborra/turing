from core import DisplayService


s = DisplayService()

try:
    s.start()

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
