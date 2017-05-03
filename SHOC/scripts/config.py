#!/usr/bin/env python
import sys
import os
import shutil


def main(directory, kernel, input_size, part, unroll, unroll_inner, pipe, cycle_time):

  print '--Running config.main()'

  d = 'p%s_u%s_ui%s_P%s_%sns' % (part, unroll, unroll_inner, pipe, cycle_time)

  print 'Kernel = %s, Part = %s, unroll = %s, unroll_inner=%s' % (kernel, part, unroll, unroll_inner)

  array_names = {
  'bb_gemm' : ['x','y','z'],
  'fft' : ['work_x','work_y','DATA_x','DATA_y','data_x','data_y','smem','reversed','sin_64','cos_64','sin_512','cos_512'],
  'md' : ['d_force_x','d_force_y','d_force_z', 'position_x','position_y','position_z','NL'],
  'pp_scan' : ['bucket','bucket2','sum'],
  'reduction' : ['in'],
  'ss_sort' : ['a','b','bucket','sum'],
  'stencil' : ['orig','sol','filter'],
  'triad'   : ['a','b','c'],
  'hotspot' : ['power','temp','result'],
  'lud1'     : ['diag'],
  'lud2'     : ['diag','peri_row','peri_col'],
  'spmv'    : ['values', 'rows', 'cols', 'vector', 'result'],
  }
  array_partition_type = {
  'bb_gemm' : ['cyclic','cyclic','cyclic'],
  'fft' : ['cyclic','cyclic','cyclic','cyclic','complete','complete','cyclic','complete','complete','complete','complete','complete'],
  'md' : ['cyclic','cyclic','cyclic','complete','complete','complete','cyclic'],
  'pp_scan' : ['cyclic','cyclic','cyclic'],
  'reduction' : ['cyclic'],
  'ss_sort' : ['cyclic','cyclic','cyclic','cyclic'],
  'stencil' : ['cyclic','cyclic','complete'],
  'triad'   : ['cyclic','cyclic','cyclic'],
  'hotspot' : ['cyclic','cyclic','cyclic'],
  'lud1'     : ['cyclic'],
  'lud2'     : ['cyclic','cyclic','cyclic'],
  'spmv'    : ['cyclic', 'cyclic', 'cyclic', 'cyclic', 'cyclic']
  }
  array_size = {
  'bb_gemm' : ['1024','1024','1024'], # large

  'fft' : ['512','512','512','512','8','8','576','8','448','448','448','448'],

  'md' : ['32', '32', '32', '32','32','32','1024'],

  'pp_scan' : ['2048','2048','128'],

  'reduction' : ['2048'], # large

  'ss_sort' : ['2048','2048','2048','128'],

  'stencil' : ['1156','1156','9'], # large

  'triad'   : ['2048','2048','2048'], # large

  'hotspot' : ['1024','1024','1024'], # large

  'lud1'     : ['1024'],

  'lud2'     : ['1024','1024','1024']

# TODO
# 'spmv'    : ['1024', '129', '1024', '128', '128'], # small
# 'spmv'    : ['2048', '129', '2048', '128', '128'], # medium
# 'spmv'    : ['2048', '129', '2048', '128', '128'], # large
  }

  # optional: reduce array size for small/medium inputs
  if input_size == 'small':
    array_size['bb_gemm'] = ['64','64','64']
    array_size['reduction'] = ['256']
    array_size['stencil'] = ['100','100','9']
    array_size['triad']   = ['256','256','256']
    array_size['hotspot']   = ['64','64','64']
    array_size['lud1']   = ['64']
    array_size['lud2']   = ['64','64','64']
  elif input_size == 'medium':
    array_size['bb_gemm'] = ['256','256','256']
    array_size['reduction'] = ['1024']
    array_size['stencil'] = ['1156','1156','9']
    array_size['triad']   = ['1024','1024','1024']
    array_size['hotspot']   = ['256','256','256']
    array_size['lud1']   = ['256']
    array_size['lud2']   = ['256','256','256']
    

  #wordsize in bytes
  #sizeof(float) = 4
  array_wordsize = {
  'bb_gemm' : ['4','4','4'],
  'fft' : ['4','4','4','4','4','4','4','4','4','4','4','4'],
  'md' : ['4', '4', '4', '4','4','4','4'],
  'pp_scan' : ['4','4','4'],
  'reduction' : ['4'],
  'ss_sort' : ['4','4','4','4'],
  'stencil' : ['4','4','4'],
  'triad'   : ['4','4','4'],
  'hotspot' : ['4','4','4'],
  'lud1'     : ['4'],
  'lud2'     : ['4','4','4'],
  'spmv'    : ['4', '4', '4', '4', '4'],
  }

  BaseFile = directory
  os.chdir(BaseFile)

  if not os.path.isdir(BaseFile + '/sim-%s/'%input_size):
    os.mkdir(BaseFile + '/sim-%s/'%input_size)

  if os.path.isdir(BaseFile + '/sim-%s/'%input_size + d):
    shutil.rmtree(BaseFile + '/sim-%s/'%input_size + d)

  if not os.path.isdir(BaseFile + '/sim-%s/'%input_size + d):
    os.mkdir(BaseFile + '/sim-%s/'%input_size + d)

  print 'Writing config file'
  config = open(BaseFile + '/sim-%s/'%input_size + d + '/config_' + d, 'w')
  config.write('cycle_time,' + cycle_time + "\n")
  print "CYCLE_TIME," + cycle_time
  config.write('pipelining,' + str(pipe) + "\n")
  #memory partition
  names = array_names[kernel]
  types = array_partition_type[kernel]
  sizes = array_size[kernel]
  wordsizes = array_wordsize[kernel]
  assert (len(names) == len(types) and len(names) == len(sizes))
  for name,type,size,wordsize in zip(names, types, sizes, wordsizes):
    if type == 'complete':
      config.write('partition,'+ type + ',' + name + ',' + \
      str(int(size)*int(wordsize)) + "\n")
    elif type == 'block' or type == 'cyclic':
      config.write('partition,'+ type + ',' + name + ',' + \
      str(int(size)*int(wordsize)) + ',' + str(wordsize) + ',' + str(part) + "\n")
    else:
      print "Unknown partition type: " + type
      sys.exit(0)
  #loop unrolling and flattening
  if kernel == 'bb_gemm':
    config.write('unrolling,bb_gemm,5,%s\n' %(unroll))
    config.write('flatten,bb_gemm,6\n' )
    config.write('flatten,bb_gemm,8\n' )

  elif kernel == 'fft':
    config.write('unrolling,step1,16,%s\n' %(unroll))
    config.write('flatten,step1,18\n')
    config.write('flatten,step1,26\n')
    config.write('flatten,step1,36\n')
    config.write('unrolling,step2,53,%s\n' %(unroll))
    config.write('flatten,step2,54\n')
    config.write('unrolling,step3,75,%s\n' %(unroll))
    config.write('flatten,step3,76\n')
    config.write('flatten,step3,83\n')
    config.write('unrolling,step4,100,%s\n' %(unroll))
    config.write('flatten,step4,101\n')
    config.write('unrolling,step5,122,%s\n' %(unroll))
    config.write('flatten,step5,123\n')
    config.write('flatten,step5,130\n')
    config.write('unrolling,step6,149,%s\n' %(unroll))
    config.write('flatten,step6,151\n')
    config.write('flatten,step6,164\n')
    config.write('flatten,step6,174\n')
    config.write('unrolling,step7,193,%s\n' %(unroll))
    config.write('flatten,step7,194\n')
    config.write('unrolling,step8,216,%s\n' %(unroll))
    config.write('flatten,step8,217\n')
    config.write('flatten,step8,224\n')
    config.write('unrolling,step9,243,%s\n' %(unroll))
    config.write('flatten,step9,244\n')
    config.write('unrolling,step10,266,%s\n' %(unroll))
    config.write('flatten,step10,267\n')
    config.write('flatten,step10,274\n')
    config.write('unrolling,step11,293,%s\n' %(unroll))
    config.write('flatten,step11,295\n')
    config.write('flatten,step11,304\n')

  elif kernel == 'md':
    config.write('unrolling,md_kernel,19,%s\n' %(unroll))

  elif kernel == 'pp_scan':
    config.write('unrolling,sum_scan,26,%s\n' %(unroll))
    config.write('unrolling,local_scan,15,%s\n' %(unroll))
    config.write('flatten,local_scan,16\n')
    config.write('unrolling,last_step_scan,33,%s\n' %(unroll))
    config.write('flatten,last_step_scan,34\n')

  elif kernel == 'reduction':
    config.write('unrolling,reduction,8,%s\n' %(unroll))

  elif kernel == 'ss_sort':
    config.write('unrolling,init,52,%s\n' %(unroll))
    config.write('unrolling,hist,61,%s\n' %(unroll))
    config.write('flatten,hist,63\n')
    config.write('unrolling,local_scan,17,%s\n' %(unroll))
    config.write('flatten,local_scan,19\n')
    config.write('unrolling,sum_scan,30,%s\n' %(unroll))
    config.write('unrolling,last_step_scan,38,%s\n' %(unroll))
    config.write('flatten,last_step_scan,40\n')
    config.write('unrolling,update,75,%s\n' % (unroll))
    config.write('flatten,update,77\n')

  elif kernel == 'stencil':
    config.write('unrolling,stencil,11,%s\n' %(unroll))
    config.write('flatten,stencil,12\n')

  elif kernel == 'triad':
    config.write('unrolling,triad,5,%s\n' %(unroll))

  elif kernel == 'hotspot':
    config.write('unrolling,hotspot,10,%s\n' %(unroll))
    config.write('flatten,hotspot,11\n')

  elif kernel == 'lud1':
    config.write('unrolling,lud1,9,%s\n' %(unroll))
    config.write('unrolling,lud1,10,%s\n' %(unroll_inner))
    #config.write('unrolling,lud1,14,%s\n' %(unroll_inner))
    config.write('unrolling,lud1,23,%s\n' %(unroll_inner))
    #config.write('unrolling,lud1,27,%s\n' %(unroll_inner))

  elif kernel == 'lud2':
    config.write('unrolling,lud2,8,%s\n' %(unroll))
    config.write('unrolling,lud2,11,%s\n' %(unroll_inner))
    config.write('unrolling,lud2,18,%s\n' %(unroll_inner))

  elif kernel == 'spmv':
    config.write('unrolling,spmv,14,%s\n' %(unroll))
    config.write('flatten,spmv,20\n')

  config.close()

if __name__ == '__main__':
  directory = sys.argv[1]
  kernel = sys.argv[2]
  input_size = sys.argv[3]
  part = sys.argv[4]
  unroll = sys.argv[5]
  pipe = sys.argv[6]
  cycle_time = sys.argv[7]
  main(directory, kernel, input_size, part, unroll, pipe, cycle_time)
