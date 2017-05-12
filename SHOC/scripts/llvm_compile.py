#!/usr/bin/env python
import os
import sys

def main (directory, source, functions, size, generalized_trace=0, loop_counts=None, unaliased_lines=None):

  if not 'TRACER_HOME' in os.environ:
    raise Exception('Set TRACER_HOME directory as an environment variable')
  out_fn = source;# + '-' + size
  os.chdir(directory)
  obj = out_fn + '.ll'
  intermed_obj = out_fn + '-intermed.ll'
  opt_obj = out_fn + '-opt.ll'
  executable = out_fn + '-instrumented'
  # set defines to determine input size
  size_define = 'SIZE_SMALL'
  if size == 'toy':
    size_define = 'SIZE_TOY'
  elif size == 'small':
    size_define = 'SIZE_SMALL'
  elif size == 'small-alias':
    size_define = 'SIZE_SMALL'
    unaliased_lines=[]
  elif size == 'medium':
    size_define = 'SIZE_MEDIUM'
  elif size == 'large':
    size_define = 'SIZE_LARGE'

  source_file = source + '.c'
  print directory

  os.system("rm -f *.ll");
  clang_cmd = 'clang -g -O1 -S -I' + os.environ['ALADDIN_HOME'] + \
        ' -D' + size_define + \
        ' -fno-slp-vectorize -fno-vectorize -fno-unroll-loops ' + \
        ' -fno-inline -fno-builtin -emit-llvm '  + source_file
        #' -fno-inline -fno-builtin -emit-llvm -o ' + obj + ' '  + source_file
  print clang_cmd
  os.system(clang_cmd)
  opt_cmd = 'opt -S -simplifycfg -indvars -loop-simplify -loop-rotate -constprop -dce -mem2reg ' + \
            ' -o ' + intermed_obj + ' ' + obj
            #' ' + obj
  print opt_cmd
  os.system(opt_cmd)

  if generalized_trace:
    # specify the possible loop counts for loop lines
    if not loop_counts is None:
      for loop_line in loop_counts.keys():
        loop_iter_str = ''
        for loop_iters in loop_counts[loop_line]:
          loop_iter_str = loop_iter_str + loop_iters + ','
    
        opt_cmd='opt -S -load=' + os.getenv('GEN_PASS_HOME') + '/lib/LLVMProj526.so ' + \
                ' -proj526 --loop_line=' + str(loop_line) + ' --iteration_counts=' + loop_iter_str + \
                ' -o ' + intermed_obj + ' ' + intermed_obj
                #' ' + obj
        print opt_cmd
        os.system(opt_cmd)

    # specify lines with unaliased accesses
    unaliased_str = ''
    if not unaliased_lines is None:
      unaliased_str = '--unaliased_lines='
      for line in unaliased_lines:
        unaliased_str = unaliased_str + line + ','

    for tgt_func in functions:
      # specify target function
      target_func_str = '--target_func=' + tgt_func
      print "got target func ", tgt_func, " in src ", source
      opt_cmd = 'opt -load=' + os.getenv('GEN_PASS_HOME') + '/lib/LLVMProj526Func.so ' + \
                ' -load=' + os.getenv('GEN_PASS_HOME') + '/lib/LLVMProj526.so ' + \
                '-nameinsts -proj526func ' + unaliased_str + ' ' + target_func_str + \
                ' -o ' + opt_obj + ' ' + intermed_obj 
                #'-nameinsts -proj526func -o ' + opt_obj + ' ' + obj 
      print opt_cmd
      os.system(opt_cmd)
      os.system('mv generalized_trace.gz generalized_trace-%s.gz' % tgt_func)
  else:
    for tgt_func in functions:
      os.environ['WORKLOAD']=tgt_func
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
      os.system('mv dynamic_trace.gz dynamic_trace-%s.gx' % tgt_func)
    

if __name__ == '__main__':
  directory = sys.argv[1]
  source = sys.argv[2]
  functions = sys.argv[3]
  size = sys.argv[4]
  print directory, source, functions, size
  main(directory, source, functions, size)
