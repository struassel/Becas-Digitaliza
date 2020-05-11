#!/usr/bin/env python3

import RequestedTasks.NetConf.utils as utils
from RequestedTasks.credentials import ios_xe1
import RequestedTasks.menu as menu
from RequestedTasks.exceptions import ConnectionError, AuthError

if __name__ == '__main__':

    try:
        menu.choose_loop([
            {"name": "Show interfaces", "cb": utils.print_interfaces, "param": ios_xe1},
            {"name": "Create Loopback interface", "cb": utils.create_interface, "param": ios_xe1},
            {"name": "Remove Loopback interface", "cb": utils.remove_interface, "param": ios_xe1},
            {"name": "Show routing table", "cb": utils.print_routing, "param": ios_xe1},
            {"name": "Show netconf statistics", "cb": utils.print_netconf_session_stats, "param": ios_xe1},
            {"name": "Show memory usage per process", "cb": utils.print_memory_usage, "param": ios_xe1}
        ], "Netconf manager")
    except (ConnectionError, AuthError) as e:
        print(e)
