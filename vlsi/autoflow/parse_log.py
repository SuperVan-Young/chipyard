import os
import re
from gen_boom_config import parse_boom_design_space
from scipy.stats import pearsonr
import numpy as np
import pandas as pd

CHIPYARD_ROOT = '/home/chenhao.xue/chipyard'

class LogParser():
    def __init__(self, config_name='TinyRocketConfig'):
        self.config_name = config_name

    def get_perf(self, benchmark_name):
        try:
            log_path = os.path.join(CHIPYARD_ROOT, f'vlsi/build/chipyard.harness.TestHarness.{self.config_name}-ChipTop/sim-rtl-rundir/{benchmark_name}/novas_dump.log')
            with open(log_path, 'r') as f:
                for line in f.readlines():
                    if 'End of simulation at' in line:
                        perf = int(line.split('End of simulation at')[1])
                        return perf
        except:
            return np.inf

    def get_power(self):
        try:
            report_path = os.path.join(CHIPYARD_ROOT, f'vlsi/build/chipyard.harness.TestHarness.{self.config_name}-ChipTop/power-rtl-rundir/waveforms.report')
            with open(report_path, 'r') as f:
                for line in f.readlines():
                    if 'Subtotal' in line:
                        total_power = float(line.strip().split(' ')[-2])
                        return total_power
        except:
            return np.inf


    def get_area(self):
        try:
            report_path = os.path.join(CHIPYARD_ROOT, f'vlsi/build/chipyard.harness.TestHarness.{self.config_name}-ChipTop/syn-rundir/reports/final_area.rpt')
            with open(report_path, 'r') as f:
                for line in f.readlines():
                    if 'BoomTile' in line:
                        total_area = float(line.strip().split(' ')[-1])
                        return total_area
        except:
            return np.inf

# legacy for analyzing synthesized results
    
def parse_all_results(ignore_invalid=True):
    boom_design_space = parse_boom_design_space()

    df = None

    for build_dir in os.listdir(os.path.join(CHIPYARD_ROOT, 'vlsi/build')):
        if 'chipyard.harness.TestHarness.Boom' not in build_dir:
            continue
        
        boom_idx = int(re.search(r'Boom(\d+)Config', build_dir).group(1))
        boom_vec = boom_design_space.idx_to_vec(boom_idx)
        boom_dict = boom_design_space.vec_to_dict(boom_vec)

        log_parser = LogParser(config_name=f"Boom{boom_idx}Config")
        perf = log_parser.get_perf('dhrystone.riscv')
        power = log_parser.get_power()
        area = log_parser.get_area()

        boom_dict['Performance'] = perf
        boom_dict['Power'] = power
        boom_dict['Area'] = area
        boom_dict['Boom Idx'] = boom_idx

        if df is None:
            df = pd.DataFrame(columns=boom_dict.keys())

        if ignore_invalid:
            if perf == np.inf: continue
            if power == np.inf: continue
            if area == np.inf: continue

        df.loc[len(df)] = boom_dict

    return df


def parse_all_area():
    boom_vec_list = []
    area_list = []

    def get_area(report_path):
        with open(report_path, 'r') as f:
            for line in f.readlines():
                if 'BoomTile' in line:
                    total_area = float(line.strip().split(' ')[-1])
                    return total_area
        raise ValueError(f'No valid area result for')

    for build_dir in os.listdir(os.path.join(CHIPYARD_ROOT, 'vlsi/build')):
        if 'chipyard.harness.TestHarness.Boom' not in build_dir:
            continue
        boom_design_space = parse_boom_design_space()
        
        boom_idx = int(re.search(r'Boom(\d+)Config', build_dir).group(1))
        boom_vec = boom_design_space.idx_to_vec(boom_idx)
        boom_dict = boom_design_space.vec_to_dict(boom_vec)

        area_report_path = os.path.join(CHIPYARD_ROOT, f'vlsi/build/{build_dir}/syn-rundir/reports/final_area.rpt')
        if not os.path.exists(area_report_path):
            print(f"path not exists: {area_report_path}")
            continue
        area = get_area(area_report_path)

        print(boom_dict)
        print(area)

        boom_vec_list.append(boom_vec)
        area_list.append(area)

    return boom_vec_list, area_list

def analyze_correlation(vec_list, res_list):
    correlations = []

    # Compute the correlation for each vector
    for vec in vec_list:
        correlation, _ = pearsonr(vec, res_list)
        correlations.append(correlation)

    boom_design_space = parse_boom_design_space()
    correlation_dict = boom_design_space.vec_to_dict(correlations)
    correlation_dict = {k: f"{v:.2f}" for k, v in correlation_dict.items()}
    
    print(f"Synthesized design point: {len(res_list)}")
    for k, v in correlation_dict.items():
        print(k, v)
    print(min(res_list))
    print(max(res_list))


    # Identify the vector with the highest correlation
    max_corr = max(correlations, default=None)
    max_index = correlations.index(max_corr) if max_corr is not None else None

    return correlations, max_index

if __name__ == '__main__':
    # boom_vec_list, area_list = parse_all_area()
    # analyze_correlation(np.transpose(boom_vec_list).tolist(), area_list)
    df = parse_all_results()
    df.to_excel("results.xlsx", index=False)
