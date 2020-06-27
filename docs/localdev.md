Setting up VirtualBox for RaspberryPi:
https://raspberrytips.com/run-raspberry-in-virtual-machine/

---

# Create the virtual machine

Launch Oracle VirtualBox now on your computer, and we will create the virtual machine:

Click on New in the top bar
Choose a Name
Type: Linux
Version: Anyone
Memory size: 1Gb is enough, but you can set more depending on your computer memory available
Hard disk: You can keep the default options (10GB)
Our new virtual machine is available, but now you have to tell it to start on the previously downloaded iso file

Click on Settings in the top bar
Select Storage in the left menu
Below the first controller, click on Empty
On the right panel, click on the Disc icon to choose the file
Select Choose Virtual Optical Disk File
Browse to the location of the image and validate

# Start the virtual machine

Now we can start the virtual machine and install the Raspberry Pi Desktop :

Click on Start in the top bar
Choose Install in the first menu
Select your Keyboard layout
For partition disks, you can keep the default options (use entire disk > all files in one partition > finish > yes)
Installation starts
After a few minutes, the installation wizard resumes
Confirm the bootloader installation to the master boot record
Select /dev/sda
Continue to reboot your new operating system
