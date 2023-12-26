import os
import re
from gen_boom_config import parse_boom_design_space
from scipy.stats import pearsonr
import numpy as np

CHIPYARD_ROOT = '/home/chenhao.xue/chipyard'

def get_area(report_path):
    with open(report_path, 'r') as f:
        for line in f.readlines():
            if 'BoomTile' in line:
                total_area = float(line.strip().split(' ')[-1])
                return total_area
    raise ValueError(f'No valid area result for')

def parse_all_area():
    boom_vec_list = []
    area_list = []

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


boom_vec_list, area_list = parse_all_area()
analyze_correlation(np.transpose(boom_vec_list).tolist(), area_list)