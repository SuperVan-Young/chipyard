# License: MIT

import os
import numpy as np
import matplotlib.pyplot as plt
from openbox import Optimizer, space as sp
from gen_boom_config import parse_boom_design_space
from parse_log import LogParser


# Define Search Space
boom_design_space = parse_boom_design_space()

def sample_condition(config):
    if not config['FetchWidth'] >= config['DecodeWidth']:
        return False
    if not config['DecodeWidth'] % config['RobEntry'] == 0:
        return False
    if not config['FetchBufferEntry'] > config['FetchWidth']:
        return False
    if not config['DecodeWidth'] % config['FetchBufferEntry']:
        return False
    if not config['FetchWidth'] == 2 * config['ICacheFetchBytes']:
        return False
    if not config['IntPhyRegister'] == config['FpPhyRegister']:
        return False
    if not config['LDQEntry'] == config['STQEntry']:
        return False
    if not config['MemIssueWidth'] == config['FpIssueWidth']:
        return False
    return True

def define_openbox_space(boom_space=boom_design_space):
    """Convert boom design space into openbox format"""
    space = sp.Space()
    for param_name, param_vals in boom_space.design_space.items():
        param = sp.Ordinal(param_name, param_vals, default_value=param_vals[0])
        space.add_variable(param)
    space.set_sample_condition(sample_condition)
    
    print(space)
    return space


# Define Objective Function
def get_ppa(idx):
    """Run vlsi flow and get results"""
    os.system("bash ./scripts/vlsi_flow.sh")
    
    boom_config_name = f"Boom{idx}Config"
    log_parser = LogParser(boom_config_name)
    
    perf = log_parser.get_perf('dhrystone.riscv')
    power = log_parser.get_power()
    area = log_parser.get_area()

    return perf, power, area

    

# Run
if __name__ == "__main__":
    space = define_openbox_space()

    opt = Optimizer(
        get_ppa,
        space,
        num_objectives=3,
        num_constraints=0,
        max_runs=50,
        surrogate_type='gp',
        acq_type='ehvi',
        acq_optimizer_type='random_scipy',
        task_id='quick_start',
    )
    history = opt.run()

    print(history)

    history.plot_convergence(true_minimum=0.397887)
    plt.show()
