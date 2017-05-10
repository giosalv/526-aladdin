#!/usr/bin/env python
import os
import sys
import os.path

import llvm_compile
import config

def main(kernel, size, part, unroll, unroll_inner, pipe, clock_period, compile_kernel, generalized_trace=0):

  if not 'ALADDIN_HOME' in os.environ:
    raise Exception('Set ALADDIN_HOME directory as an environment variable')

  if not 'TRACER_HOME' in os.environ:
    raise Exception('Set TRACER_HOME directory as an environment variable')

  if not 'GEN_PASS_HOME' in os.environ:
    raise Exception('Set GEN_PASS_HOME directory as an environment variable')


  ALADDIN_HOME = os.getenv('ALADDIN_HOME')
  BENCH_HOME = ALADDIN_HOME + '/SHOC/' + kernel

  os.chdir(BENCH_HOME)
  d = 'p%s_u%s_ui%s_P%s_%sns' % (part, unroll, unroll_inner, pipe, clock_period)
  print d, compile_kernel, generalized_trace

  #Run LLVM-Tracer to generate the dynamic trace
  #Only need to run once to generate the design space of each algorithm
  #All the Aladdin runs use the same trace
  if compile_kernel == "True":
    llvm_compile.main(BENCH_HOME, kernel, size)

  #Generate accelerator design config file
  config.main(BENCH_HOME, kernel, size, part, unroll, unroll_inner, pipe, clock_period, generalized_trace)

  print 'Start Aladdin'
  trace_file = ''
  aladdin_exec = ''
  if generalized_trace:
    trace_file = BENCH_HOME+ '/' + 'generalized_trace.gz'
    aladdin_exec = 'aladdin-generalized'
  else:
    trace_file = BENCH_HOME+ '/' + 'dynamic_trace.gz'
    aladdin_exec = 'aladdin'
  config_file = 'config_' + d

  if generalized_trace:
    newdir = os.path.join(BENCH_HOME, 'sim-general', d)
  else:
    newdir = os.path.join(BENCH_HOME, 'sim-%s'%size, d)
  print 'Changing directory to %s' % newdir

  os.chdir(newdir)
  exec_cmd = ('%s/common/%s %s %s %s' % \
                (os.getenv('ALADDIN_HOME'), aladdin_exec, kernel, trace_file, config_file))
  print(exec_cmd)
  os.system(exec_cmd)

  for file in os.listdir("."):
    if file.endswith(".dot"):
      base = file[0:-4]
      graph_cmd = 'dot -Tpdf -o %s.pdf %s' % (base, file)
      print graph_cmd
      os.system(graph_cmd)

if __name__ == '__main__':
  kernel = sys.argv[1]
  size = sys.argv[2]
  part = sys.argv[3]
  unroll = sys.argv[4]
  unroll_inner = sys.argv[5]
  pipe = sys.argv[6]
  clock_period = sys.argv[7]
  compile_kernel = sys.argv[8]
  generalized_trace = int(sys.argv[9])
  main(kernel, size, part, unroll, unroll_inner, pipe, clock_period, compile_kernel, generalized_trace)

