## automating_framwork

I kind of want to start automating my workflows now, so I've been working on individual ways to automate devices I have to configure as part of my job.


# Cisco Small Business Switches:

Netmiko is best. Another way to make configuration easier in a bigger environment with a lot of engineers is to:

1. Set up a config TFTP server
2. Set up Git to be able to push changes to that server
3. Build configs
4. Git Push
5. Run a While Loop on your network with a for loop iterating over your configs.

This is a good way to take my simple script and turn it into something pretty nice.

# Other Devices

TBD....