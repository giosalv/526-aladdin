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
'hello'    : 'hello',
}

def main (directory, source, size, generalized_trace=0, loop_counts=None):

  if not 'TRACER_HOME' in os.environ:
    raise Exception('Set TRACER_HOME directory as an environment variable')
  out_fn = source;# + '-' + size
  os.chdir(directory)
  obj = out_fn + '.ll'
  intermed_obj = out_fn + '-intermed.ll'
  opt_obj = out_fn + '-opt.ll'
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

  clang_cmd = 'clang -g -O0 -S -I' + os.environ['ALADDIN_HOME'] + \
        ' -D' + size_define + \
        ' -fno-slp-vectorize -fno-vectorize -fno-unroll-loops ' + \
        ' -fno-inline -fno-builtin -emit-llvm '  + source_file
        #' -fno-inline -fno-builtin -emit-llvm -o ' + obj + ' '  + source_file
  print clang_cmd
  os.system(clang_cmd)
  opt_cmd = 'opt -S -simplifycfg -indvars -loop-simplify -loop-rotate -dce -licm -mem2reg  ' + \
            ' -o ' + intermed_obj + ' ' + obj
            #' ' + obj
  print opt_cmd
  os.system(opt_cmd)

  if generalized_trace:
    if not loop_counts is None:
      for loop_line in loop_counts.keys():
        loop_iter_str = ''
        for loop_iters in loop_counts[loop_line]:
          loop_iter_str = loop_iter_str + loop_iters + ","
    
        opt_cmd='opt -S -load=' + os.getenv('GEN_PASS_HOME') + '/lib/LLVMProj526.so ' + \
                ' -proj526 --loop_line=' + str(loop_line) + ' --iteration_counts=' + loop_iter_str + \
                ' -o ' + intermed_obj + ' ' + intermed_obj
                #' ' + obj
        print opt_cmd
        os.system(opt_cmd)
    opt_cmd = 'opt -load=' + os.getenv('GEN_PASS_HOME') + '/lib/LLVMProj526Func.so ' + \
              ' -load=' + os.getenv('GEN_PASS_HOME') + '/lib/LLVMProj526.so ' + \
              '-nameinsts -proj526func -o ' + opt_obj + ' ' + intermed_obj 
              #'-nameinsts -proj526func -o ' + opt_obj + ' ' + obj 
    print opt_cmd
    os.system(opt_cmd)
  else:
    opt_cmd = 'opt -S -load=' + os.getenv('TRACER_HOME') + '/full-trace/full_trace.so -fulltrace -labelmapwriter ' + intermed_obj + ' -o ' + intermed_obj
    print opt_cmd
    os.system(opt_cmd)

    print 'llvm-link -o full.llvm ' + intermed_obj + ' ' + os.getenv('TRACER_HOME') + '/profile-func/trace_logger.llvm'
    os.system('llvm-link -o full.llvm ' + intermed_obj + ' ' + os.getenv('TRACER_HOME') + '/profile-func/trace_logger.llvm')

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
