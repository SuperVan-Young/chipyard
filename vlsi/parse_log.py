import os
import argparse

CHIPYARD_DIR = '/root/chipyard/'

parser = argparse.ArgumentParser()
parser.add_argument('--config_name', type=str, default='TinyRocketConfig', help='Processor design config name')
args = parser.parse_args()

class LogParser():
    def __init__(self, config_name='TinyRocketConfig'):
        self.config_name = config_name

    def get_perf(self, benchmark_name):
        log_path = os.path.join(CHIPYARD_DIR, f'vlsi/build/chipyard.harness.TestHarness.{self.config_name}-ChipTop/sim-rtl-rundir/{benchmark_name}/novas_dump.log')
        with open(log_path, 'r') as f:
            for line in f.readlines():
                if 'End of simulation at' in line:
                    perf = int(line.split('End of simulation at')[1])
                    return perf
        raise ValueError(f'No valid performance result for {benchmark_name}')

    def get_power(self):
        report_path = os.path.join(CHIPYARD_DIR, f'vlsi/build/chipyard.harness.TestHarness.{self.config_name}-ChipTop/power-rtl-rundir/waveforms.report')
        with open(report_path, 'r') as f:
            for line in f.readlines():
                if 'Subtotal' in line:
                    total_power = line.strip().split(' ')[-2]
                    return total_power
        raise ValueError(f'No valid area result for')


    def get_area(self):
        report_path = os.path.join(CHIPYARD_DIR, f'vlsi/build/chipyard.harness.TestHarness.{self.config_name}-ChipTop/syn-rundir/reports/final_area.rpt')
        with open(report_path, 'r') as f:
            for line in f.readlines():
                if 'BoomTile' in line:
                    total_area = float(line.strip().split(' ')[-1])
                    return total_area
        raise ValueError(f'No valid area result for')

    def summarize(self):
        try:
            area = self.get_area()
        except ValueError:
            area = 'Error'
        print(f"Area: {area}")

        benchmarks = ['dhrystone.riscv']
        for benchmark_name in benchmarks:
            try:
                perf = self.get_perf(benchmark_name)
            except ValueError:
                perf = 'Error'
            print(f"Perf ({benchmark_name}): {perf}")

        try:
            power = self.get_power()
        except ValueError:
            power = 'Error'
        print(f"Power: {power}")


log_parser = LogParser(config_name=args.config_name)
log_parser.summarize()