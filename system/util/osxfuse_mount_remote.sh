# You'll need to first create the directory that serves as the mount proxy (/pi
# in the case of below)

sshfs pi@10.0.1.51:/home/pi ~/Desktop/turing-pi -o defer_permissions -o volname=turing-pi
