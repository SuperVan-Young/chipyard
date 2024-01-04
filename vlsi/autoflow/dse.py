# License: MIT

import os
import numpy as np
import matplotlib.pyplot as plt
import random
import openbox
import subprocess
import fcntl
from openbox import Optimizer, ParallelOptimizer, space as sp
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


def generate_chisel_code(idx):
    """Check if config index is unique, synchronize with a file
    """
    UNIQUE_IDX_FILE = "./unique_idx.txt"
    if not os.path.exists(UNIQUE_IDX_FILE):
        os.system(f'touch {UNIQUE_IDX_FILE}')

    with open(UNIQUE_IDX_FILE, 'r+') as file:
        # lock the file atomically
        fcntl.flock(file.fileno(), fcntl.LOCK_SH)

        history_idx_list = [int(line.strip()) for line in file.readlines()]
        if idx not in history_idx_list:
            history_idx_list.append(idx)
            file.seek(0, os.SEEK_END)
            file.write(f"{idx}\n")

        fcntl.flock(file.fileno(), fcntl.LOCK_UN)

    boom_design_space.generate_chisel_codes(history_idx_list)


# Define Objective Function
def get_ppa(config):
    """Run vlsi flow and get results"""
    vec = boom_design_space.dict_to_vec(config)
    idx = boom_design_space.vec_to_idx(vec)

    openbox.logger.info(config)

    # generate configuration file before running the flow
    generate_chisel_code(idx)

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

    # opt = Optimizer(
    #     get_ppa,
    #     space,
    #     num_objectives=3,
    #     num_constraints=0,
    #     max_runs=50,
    #     surrogate_type='gp',
    #     acq_type='ehvi',
    #     acq_optimizer_type='random_scipy',
    #     task_id='BOOM Explorer',
    #     ref_point=(15000000000, 50, 5000000),
    #     random_state=1,
    # )

    opt = ParallelOptimizer(
        get_ppa,
        space,
        parallel_strategy='async',
        batch_size=4,
        batch_strategy='default',
        num_objectives=3,
        num_constraints=0,
        max_runs=100,
        surrogate_type='gp',
        acq_type='ehvi',
        acq_optimizer_type='random_scipy',
        task_id='BOOM Explorer',
        ref_point=(15000000000, 50, 5000000),
        random_state=1,
    )

    history = opt.run()

    history.plot_convergence()
    plt.show()
