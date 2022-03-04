# Kindle Clock

This was only tested on 4th generation Kindle, firmware version 4.1.4. I don't know if it works with other devices or firmware version.

## How to
### Jailbreak
* Plug in the Kindle and copy the content of the `jailbreak` folder in `bin.zip` to the Kindle's USB drive's root 
* Safely remove the USB cable and restart the Kindle ([Menu] -> Settings -> [Menu] -> Restart)
* Once the device restarts into diagnostics mode, select "D) Exit, Reboot or Disable Diags" (using the 5-way keypad) 
* Select "R) Reboot System" and "Q) To continue" (following on-screen instructions, when it tells you to use 'FW Left' to select an option, it means left on the 5-way keypad) 
* Wait about 20 seconds: you should see the Jailbreak screen for a while, and the device should then restart normally 
* After the Kindle restarts, you should see a new book titled "You are Jailbroken", if you see this, the jailbreak has been successful

### Enabling SSH
* Plug in the Kindle and copy the content of the `usbnetwork` folder in `bin.zip` to the Kindle's USB drive's root 
* Safely remove the USB cable and update the Kindle ([Menu] -> Settings -> [Menu] -> Update Your Kindle)
* Once the device restarts, plug in the Kindle and setup your public key in `usbnet/etc/authorized_keys`
* Edit `usbnet/etc/config` and set `K3_WIFI="true"` and `USE_OPENSSH="true"`
* Safely remove the USB cable
* Test if the connection via SSH works
    * Press the keyboard key on the Kindle and write `;debugOn` followed by enter
    * Press the keyboard key on the Kindle and write `~usbNetwork` followed by enter
    * Now try connecting to the Kindle via SSH (with root user)
* If SSH connection works, enable USBnetwork at system startup by creating a blank `auto` file in the `usbnet` folder 
    * You can use the command `touch /mnt/us/usbnet/auto`
    * Warning: this will disable USB mass storage, so be sure that everything is working as it should!
* Reboot the device and test if SSH works at startup

### Installing Python and screen
* Plug in the Kindle and copy the content of the `python` in `bin.zip` folder to the Kindle's USB drive's root 
* Safely remove the USB cable and update the Kindle ([Menu] -> Settings -> [Menu] -> Update Your Kindle)
* Once the device restarts, install pip by running `python3 -m ensurepip --upgrade`
* Copy the content of the `screen` folder in `bin.zip` to `/mnt/us/bin`
* Create a symlink for using screen system-wide `ln -s /mnt/us/bin/screen /usr/bin/screen`

### Installing and running the software
* Clone this repository in `/mnt/us/dashboard`
* Install requirements by running `python3 -m pip install -r /mnt/us/dashboard/requirements.txt`
* Run `/mnt/us/dashboard/start.sh`

### Start on boot
* Work in progress...

### Update time
* To syncronize clock: `ntpdate 0.it.pool.ntp.org`
* If you want to change the timezone, you must edit `/etc/localtime`
    * Copy the timezone file you want from a Linux system (for example: `/usr/share/zoneinfo/Europe/Rome`) to /mnt/us/
    * Remove the old symlink `rm /etc/localtime`
    * Symlink to the new timezone: `ln -s /mnt/us/Rome /etc/localtime`

## Source
* Kindle jailbreak: https://wiki.mobileread.com/wiki/Kindle4NTHacking#Jailbreak
* USBNetwork: https://www.mobileread.com/forums/showthread.php?t=88004
* Python: https://www.mobileread.com/forums/showthread.php?t=225030
* screen: https://www.fabiszewski.net/kindle-terminal/