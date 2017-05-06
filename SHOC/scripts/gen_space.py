#!/usr/bin/env python

import numpy as np
import sys
import os
import os.path
import math
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt

import llvm_compile

gen_results = 1
graph_results = 0

#unroll = [1, 2, 4, 8, 16, 32]#, 64]
unroll = [1]#, 4, 16, 64]
unroll_inner = [1]#, 4, 16, 64]
#part  = [1, 2, 4, 8, 16, 32]#, 64]
part = [1]#, 4, 16, 64]
pipe = [0]#, 1]

#You can parallel this by running multiply jobs together
#In this case, llvm_coompile.py inside run_aladdin.py only need to run once
#to generate the dynamic instruction trace


# SHOC original
#benchmarks = ['triad', 'reduction', 'stencil', 'fft', 'md', 'pp_scan', 'bb_gemm']

# 598
#benchmarks = ['bb_gemm', 'hotspot', 'lud', 'reduction', 'spmv', 'stencil', 'triad']
#benchmarks = ['bb_gemm', 'hotspot', 'lud1', 'lud2', 'reduction', 'stencil', 'triad']

# debug
#benchmarks = ['spmv']
benchmarks = ['lud1','lud2','stencil']
sizes = ['small','medium','large']

generalized_trace = 1
benchmarks = ['hello']
sizes = ['small']
loop_counts={}
loop_counts['hello'] = {}
loop_counts['hello']['5'] = ['6']

ALADDIN_HOME = str(os.getenv('ALADDIN_HOME'))
GEN_PASS_HOME = str(os.getenv('GEN_PASS_HOME'))

for bench in benchmarks:
  for size in sizes:
    print bench+'-'+size

    # MH: Compile the benchmark once before the loop, instead of compiling it
    # for every single configuration.
    BENCH_HOME = ALADDIN_HOME + '/SHOC/' + bench
    llvm_compile.main(BENCH_HOME, bench, size, generalized_trace, loop_counts[bench])
    os.chdir(ALADDIN_HOME + '/SHOC/scripts')

    if gen_results:
      for f_unroll in unroll:
        for f_unroll_inner in unroll_inner:
          # never unroll inner more than outer loop
          if f_unroll < f_unroll_inner:
            continue
          for f_part in part:
            for f_pipe in pipe:
              # CHANGE CLOCK FREQUENCY HERE. CURRENTLY 2 NS.
              os.system('python run_aladdin.py %s %s %i %i %i %i 2 False %d' % (bench, size, f_part, f_unroll, f_unroll_inner, f_pipe, generalized_trace))

    if graph_results:
      MAX_VAL = 0xFFFFFFFF
      cycle = []
      total_power = []
      fu_power = []
      mem_power = []
      total_area = []
      fu_area = []
      mem_area = []
      cycle_min_idx = 0
      total_power_min_idx = 0
      fu_power_min_idx = 0
      mem_power_min_idx = 0
      total_area_min_idx = 0
      fu_area_min_idx = 0
      mem_area_min_idx = 0
      cp_min_idx = 0
      ccp_min_idx = 0
      ca_min_idx = 0
      pa_min_idx = 0
      cycle_min_config = '?'
      total_power_min_config = '?'
      fu_power_min_config = '?'
      mem_power_min_config = '?'
      total_area_min_config = '?'
      fu_area_min_config = '?'
      mem_area_min_config = '?'
      cp_min_config = '?'
      ccp_min_config = '?'
      ca_min_config = '?'
      pa_min_config = '?'

      if not os.path.exists(ALADDIN_HOME + '/SHOC/scripts/data-%s/'%size):
        os.makedirs(ALADDIN_HOME + '/SHOC/scripts/data-%s/'%size)

      os.chdir(BENCH_HOME + '/sim-%s/'%size)

      dirs = os.listdir(BENCH_HOME + '/sim-%s/'%size)

      dir_list = []
      for d in dirs:
        #if os.path.isfile(d + '/' + bench + '_summary'):
        if os.path.isfile(d + '/' + '_summary'):
          #file = open( d + '/' + bench  + '_summary', 'r')
          file = open( d + '/' + '_summary', 'r')
          dir_list.append(d)
          for line in file:

            if 'Cycle' in line:
              curr_cycle = int(line.split(' ')[2])
              cycle.append(curr_cycle)
              if curr_cycle <= cycle[cycle_min_idx]:
                cycle_min_idx = len(cycle)-1
                cycle_min_config = d
            elif 'Avg Power' in line:
              curr_power = float(line.split(' ')[2])
              total_power.append(curr_power)
              if curr_power <= total_power[total_power_min_idx]:
                total_power_min_idx = len(total_power)-1
                total_power_min_config = d
            elif 'Avg FU Power' in line:
              curr_fu_power = float(line.split(' ')[3])
              fu_power.append(curr_fu_power)
              if curr_fu_power <= fu_power[fu_power_min_idx]:
                fu_power_min_idx = len(fu_power)-1
                fu_power_min_config = d
            elif 'Avg MEM Power' in line:
              curr_mem_power = float(line.split(' ')[3])
              mem_power.append(curr_mem_power)
              if curr_mem_power <= mem_power[mem_power_min_idx]:
                mem_power_min_idx = len(mem_power)-1
                mem_power_min_config = d
            elif 'Total Area' in line:
              curr_area = float(line.split(' ')[2])
              total_area.append(curr_area)
              if curr_area <= total_area[total_area_min_idx]:
                total_area_min_idx = len(total_area)-1
                total_area_min_config = d
            elif 'FU Area' in line:
              curr_fu_area = float(line.split(' ')[2])
              fu_area.append(curr_fu_area)
              if curr_fu_area <= fu_area[fu_area_min_idx]:
                fu_area_min_idx = len(fu_area)-1
                fu_area_min_config = d
            elif 'MEM Area' in line:
              curr_mem_area = float(line.split(' ')[2])
              mem_area.append(curr_mem_area)
              if curr_mem_area <= mem_area[mem_area_min_idx]:
                mem_area_min_idx = len(mem_area)-1
                mem_area_min_config = d
            else:
              continue
          file.close()
      
      # determine composite minimums (delay*power, delay^2*power)
      curr_idx = 0
      for (curr_cycles, curr_power, curr_area) in zip(cycle, total_power, total_area):
        if curr_cycles * curr_power < cycle[cp_min_idx] * total_power[cp_min_idx]:
          cp_min_idx = curr_idx
          cp_min_config = dir_list[curr_idx]
        if curr_cycles * curr_cycles * curr_power < cycle[ccp_min_idx] * cycle[ccp_min_idx] * total_power[ccp_min_idx]:
          ccp_min_idx = curr_idx
          ccp_min_config = dir_list[curr_idx]
        if curr_cycles * curr_area < cycle[ca_min_idx] * total_area[ca_min_idx]:
          ca_min_idx = curr_idx
          ca_min_config = dir_list[curr_idx]
        if curr_power * curr_area < total_power[pa_min_idx] * total_area[pa_min_idx]:
          pa_min_idx = curr_idx
          pa_min_config = dir_list[curr_idx]
        curr_idx += 1

      colors = ['k', 'c', 'g', 'b', 'm', 'r']

      os.chdir(ALADDIN_HOME + '/SHOC/scripts/data-%s/'%size)
      fig = plt.figure()
      fig.suptitle('SHOC ' + bench + ' Total Power Design Space')
      curr_plot = fig.add_subplot(111)
      scatter_all = curr_plot.scatter(cycle, total_power, color=colors[0])
      minc = curr_plot.scatter([cycle[cycle_min_idx]], [total_power[cycle_min_idx]], color=colors[1])
      minp = curr_plot.scatter([cycle[total_power_min_idx]], [total_power[total_power_min_idx]], color=colors[2])
      mincp = curr_plot.scatter([cycle[cp_min_idx]], [total_power[cp_min_idx]], color=colors[3])
      minccp = curr_plot.scatter([cycle[ccp_min_idx]], [total_power[ccp_min_idx]], color=colors[4])
      curr_plot.legend((scatter_all, minc, minp, mincp, minccp),
                       ('all', 'min c:'+cycle_min_config, 'min p:'+total_power_min_config, 'min E:'+cp_min_config, 'min ED:'+ccp_min_config),
                       scatterpoints=1, loc='upper right',
                       ncol=1, fontsize=8)
      curr_plot.set_xlabel('Cycles')
      curr_plot.set_ylabel('Total Power (mW)')
      curr_plot.grid(True)
      plt.savefig(bench + '-cycles-total-power.pdf')

      fig = plt.figure()
      fig.suptitle('SHOC ' + bench + ' FU Power Design Space')
      curr_plot = fig.add_subplot(111)
      curr_plot.scatter(cycle, fu_power)
      curr_plot.scatter(cycle, fu_power)
      curr_plot.set_xlabel('Cycles')
      curr_plot.set_ylabel('FU Power (mW)')
      curr_plot.grid(True)
      plt.savefig(bench + '-cycles-fu-power.pdf')

      fig = plt.figure()
      fig.suptitle('SHOC ' + bench + ' MEM Power Design Space')
      curr_plot = fig.add_subplot(111)
      curr_plot.scatter(cycle, mem_power)
      curr_plot.set_xlabel('Cycles')
      curr_plot.set_ylabel('MEM Power (mW)')
      curr_plot.grid(True)
      plt.savefig(bench + '-cycles-mem-power.pdf')


      fig = plt.figure()
      fig.suptitle('SHOC ' + bench + ' Total Area Design Space')
      curr_plot = fig.add_subplot(111)
      scatter_all = curr_plot.scatter(cycle, total_area, color=colors[0])
      minc = curr_plot.scatter([cycle[cycle_min_idx]], [total_area[cycle_min_idx]], color=colors[1])
      mina = curr_plot.scatter([cycle[total_area_min_idx]], [total_area[total_area_min_idx]], color=colors[2])
      minca = curr_plot.scatter([cycle[ca_min_idx]], [total_area[ca_min_idx]], color=colors[3])
      curr_plot.legend((scatter_all, minc, mina, minca),
                       ('all', 'min c:'+cycle_min_config, 'min a:'+total_area_min_config, 'min c*a:'+ca_min_config),
                       scatterpoints=1, loc='upper right',
                       ncol=1, fontsize=8)
      curr_plot.set_xlabel('Cycles')
      curr_plot.set_ylabel('Total Area (uM^2)')
      curr_plot.grid(True)
      plt.savefig(bench + '-cycles-total-area.pdf')

      fig = plt.figure()
      fig.suptitle('SHOC ' + bench + ' FU Area Design Space')
      curr_plot = fig.add_subplot(111)
      curr_plot.scatter(cycle, fu_area)
      curr_plot.set_xlabel('Cycles')
      curr_plot.set_ylabel('FU Area (uM^2)')
      curr_plot.grid(True)
      plt.savefig(bench + '-cycles-fu-area.pdf')

      fig = plt.figure()
      fig.suptitle('SHOC ' + bench + ' MEM Area Design Space')
      curr_plot = fig.add_subplot(111)
      curr_plot.scatter(cycle, mem_area)
      curr_plot.set_xlabel('Cycles')
      curr_plot.set_ylabel('MEM Area (uM^2)')
      curr_plot.grid(True)
      plt.savefig(bench + '-cycles-mem-area.pdf')
      os.chdir(ALADDIN_HOME + '/SHOC/scripts/')
