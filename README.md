## arkOS Beacon

This is a simple server app that keeps a socket open on the device, responds with basic information, and can run lowlevel actions (i.e. restart Genesis, restart or shutdown the arkOS node itself).

The idea behind this was to allow the arkOS Installer to scan the network for arkOS nodes, and instantly find them along with their IP addresses. Also provides a good option to reboot the Pi if there is a problem with Genesis and you don't have physical access.
