# Set up VirtualBox
http://www.penguintutor.com/raspberrypi/rpi-desktop-virtualbox

From the VirtualBox menu at the top of the VirtualMachine click on Devices -> Insert Guest Additions CD Image. You should then see a pop-up saying that a removal medium is inserted (which is acting as though a CD has been inserted into a virtual drive).

# Install Guest Additions on virtual Raspberry Pi machine
Run the following commands on the command line:
cd /media/cdrom0
sudo bash VBoxLinuxAdditions.run

