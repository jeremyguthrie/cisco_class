This is the script CDW wrote for their week-1 ACI workshop.

The purpose of this script is to walk a network given a seed switch,
gather learned ARP addresses, learned MAC addresses, and switch names
to build a map of IPs -> MAC Addresses -> switchports on switches.

It cannot differentiate between VRFs but it will build a list of IPs
and MACs when there are duplicates.
