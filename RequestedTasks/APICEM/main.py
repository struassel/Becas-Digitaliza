#!/usr/bin/env python3

import RequestedTasks.APICEM.utils as utils
from RequestedTasks.credentials import apic_endpoints
import RequestedTasks.menu as menu
from RequestedTasks.exceptions import ConnectionError, AuthError, DataError

if __name__ == '__main__':
    try:
        try:
            utils.print_apic_endpoints(apic_endpoints)
            opt = int(input("Choose option: "))

            if opt < 0 or opt > len(apic_endpoints):
                raise ValueError()

        except (ValueError, DataError):
            print("Invalid option, try again")
            exit()

        menu.choose_loop([
            {"name": "Show hosts", "cb": utils.print_hosts, "param": apic_endpoints[opt]},
            {"name": "Show devices", "cb": utils.print_devices, "param": apic_endpoints[opt]},
            {"name": "Show reachability info", "cb": utils.print_reachability_info, "param": apic_endpoints[opt]},
            {"name": "Show interfaces", "cb": utils.print_interfaces, "param": apic_endpoints[opt]},
            {"name": "Show device interfaces", "cb": utils.print_interfaces_of_device, "param": apic_endpoints[opt]}
        ], "APIC-Enterprise Module")
    except (ConnectionError, AuthError) as e:
        print(e)
