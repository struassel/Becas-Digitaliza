#!/usr/bin/env python3
import RequestedTasks.Calculator.utils as utils
import RequestedTasks.menu as menu

if __name__ == '__main__':
    menu.choose_loop([
        {"name": "Add", "cb": utils.add},
        {"name": "Substract", "cb": utils.subtract},
        {"name": "Multiply", "cb": utils.multiply},
        {"name": "Divide", "cb": utils.divide},
        {"name": "Power", "cb": utils.power},
        {"name": "Sqr", "cb": utils.sqrt},
        {"name": "Factorial", "cb": utils.factorial},
        {"name": "Log", "cb": utils.log},
        {"name": "Sin", "cb": utils.sin},
        {"name": "Cos", "cb": utils.cos},
        {"name": "Tan", "cb": utils.tan},
    ], "Calculator")
