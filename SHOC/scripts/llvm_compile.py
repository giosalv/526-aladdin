#!/usr/bin/env python
import os
import sys

kernels = {
'bb_gemm' : 'bb_gemm',
'fft' : 'fft1D_512,step1,step2,step3,step4,step5,step6,step7,step8,step9,step10,step11',
'md' : 'md,md_kernel',
'pp_scan' : 'pp_scan,local_scan,sum_scan,last_step_scan',
'reduction' : 'reduction',
'ss_sort' : 'ss_sort,init,hist,local_scan,sum_scan,last_step_scan,update',
'stencil' : 'stencil',
'triad'   : 'triad',
'hotspot' : 'hotspot',
'lud1'     : 'lud1',
'lud2'     : 'lud2',
'spmv'    : 'spmv',
}

def main (directory, source, size):

  if not 'TRACER_HOME' in os.environ:
    raise Exception('Set TRACER_HOME directory as an environment variable')
  out_fn = source + '-' + size
  os.chdir(directory)
  obj = out_fn + '.llvm'
  opt_obj = out_fn + '-opt.llvm'
  executable = out_fn + '-instrumented'
  os.environ['WORKLOAD']=kernels[source]
  # set defines to determine input size
  size_define = 'SIZE_SMALL'
  if size == 'small':
    size_define = 'SIZE_SMALL'
  elif size == 'medium':
    size_define = 'SIZE_MEDIUM'
  elif size == 'large':
    size_define = 'SIZE_LARGE'

  source_file = source + '.c'
  print directory

  print 'clang -g -O1 -S -I' + os.environ['ALADDIN_HOME'] + \
        ' -D' + size_define + \
        ' -fno-slp-vectorize -fno-vectorize -fno-unroll-loops ' + \
        ' -fno-inline -fno-builtin -emit-llvm -o ' + obj + ' '  + source_file
  os.system('clang -g -O1 -S -I' + os.environ['ALADDIN_HOME'] + \
            ' -D' + size_define + \
            ' -fno-slp-vectorize -fno-vectorize -fno-unroll-loops ' + \
            ' -fno-inline -fno-builtin -emit-llvm -o ' + obj + ' ' + source_file)

  print 'opt -S -load=' + os.getenv('TRACER_HOME') + '/full-trace/full_trace.so -fulltrace ' + obj + ' -o ' + opt_obj
  os.system('opt -S -load=' + os.getenv('TRACER_HOME') + '/full-trace/full_trace.so -fulltrace ' + obj + ' -o ' + opt_obj)

  print 'llvm-link -o full.llvm ' + opt_obj + ' ' + os.getenv('TRACER_HOME') + '/profile-func/trace_logger.llvm'
  os.system('llvm-link -o full.llvm ' + opt_obj + ' ' + os.getenv('TRACER_HOME') + '/profile-func/trace_logger.llvm')

  print 'llc -O0 -disable-fp-elim -filetype=asm -o full.s full.llvm'
  os.system('llc -O0 -disable-fp-elim -filetype=asm -o full.s full.llvm')

  print 'gcc -O0 -fno-inline -o ' + executable + ' full.s -lm -lz'
  os.system('gcc -O0 -fno-inline -o ' + executable + ' full.s -lm -lz')

  print './' + executable
  os.system('./' + executable)

if __name__ == '__main__':
  directory = sys.argv[1]
  source = sys.argv[2]
  size = sys.argv[3]
  print directory, source, size
  main(directory, source, size)
