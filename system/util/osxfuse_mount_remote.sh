# You'll need to first create the directory that serves as the mount proxy (/pi
# in the case of below)

sudo sshfs -o allow_other,defer_permissions pi@10.0.1.51:/ ~/projects/dolly-proxy/ -o volname=dolly-proxy
