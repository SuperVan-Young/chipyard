# License: MIT

import os
import numpy as np
import matplotlib.pyplot as plt
import random
import openbox
import subprocess
from openbox import Optimizer, space as sp
from gen_boom_config import parse_boom_design_space
from parse_log import LogParser


# Define Search Space
boom_design_space = parse_boom_design_space()

def sample_condition(config):
    return boom_design_space.dic_is_valid(config)

def define_openbox_space(boom_space=boom_design_space):
    """Convert boom design space into openbox format"""
    space = sp.ConditionedSpace()
    for param_name, param_vals in boom_space.design_space.items():
        param = sp.Ordinal(param_name, param_vals, default_value=param_vals[0])
        space.add_variable(param)
    # print(space)
    space.set_sample_condition(sample_condition)
    
    return space

def run_subprocess(cmd):
    result = subprocess.run(cmd, text=True, shell=True)

    # 检查返回值
    if result.returncode == 0:
        return 0
    else:
        raise RuntimeError(f"Failure in running subprocess {cmd}, return code", result.returncode)

# Define Objective Function
def get_ppa(config):
    """Run vlsi flow and get results"""
    vec = boom_design_space.dict_to_vec(config)
    idx = boom_design_space.vec_to_idx(vec)

    openbox.logger.info(config)

    # generate configuration file before running the flow
    boom_design_space.generate_chisel_codes([idx])

    # os.system(f"bash ./scripts/vlsi_flow.sh {idx}")
    cmd = f"bash ./scripts/vlsi_flow.sh {idx}"
    run_subprocess(cmd)
    
    boom_config_name = f"Boom{idx}Config"
    log_parser = LogParser(boom_config_name)
    
    perf = log_parser.get_perf('dhrystone.riscv')
    power = log_parser.get_power()
    area = log_parser.get_area()

    result = dict()
    result['objectives'] = np.array((perf, power, area))
    return result

def pseudo_get_ppa(config):
    openbox.logger.info(config)

    perf = random.randint(100000, 500000)
    power = random.random() * 0.1
    area = random.randint(1000000, 3500000)

    result = dict()
    result['objectives'] = np.array((perf, power, area))
    return result
    
def test_get_ppa():
    test_idx = 1730202087
    test_vec = boom_design_space.idx_to_vec(test_idx)
    test_config = boom_design_space.vec_to_dict(test_vec)
    result = get_ppa(test_config)
    print(result)

# Run
if __name__ == "__main__":
    # test_get_ppa()

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
        task_id='BOOM Explorer',
        ref_point=(500000, 0.10, 5000000),
        random_state=1,
    )
    history = opt.run()

    print(history)

    history.plot_convergence(true_minimum=0.397887)
    plt.show()
