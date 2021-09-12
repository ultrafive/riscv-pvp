#!/usr/bin/env python3

import sys
import subprocess
import numpy as np
import jax.numpy as jnp

# find the result from the start location of signature file
def from_txt(fpath, golden, start ):
    ebyte = golden.itemsize
    size = golden.size
    dtype = golden.dtype
    # we need to save the result align ebyte so we need align_size here
    align_size = ebyte

    if golden.dtype == np.bool_:
        # set ebyte to 0.1 to be different with e8
        ebyte = 0.1
        align_size = 1

    result = []
    now = 0
    # we recompute the start location in order to satisfy the align mechanism
    if start % align_size != 0:
        start = ( start // align_size + 1 ) * align_size
    with open(fpath) as file:
        for line in file:
            line = line.rstrip()
            if start - now >= 32:
                # if start bigger than this line, continue to next line
                now += 32
                continue
            else:  
                # if start is in this line, we use start-now as line_start
                # if not we use 0 as line_start                
                line_start = start - now
                if line_start < 0:
                    line_start = 0    

                if ebyte != 0.1:
                    # handle e8\e16\e32\e64
                    while line_start != 32:
                        # we get hex string from end to start because they are saved in that way
                        if line_start == 0:
                            str = line[-2*ebyte:]
                        else:
                            str = line[-2*(ebyte+line_start): -2*line_start]
                        line_start += ebyte
                        num = int( str, 16 )
                        result.append( num )                    

                else:
                    # handle mask register
                    # every hex char have 4 bits
                    for no in range(2*line_start, 64):
                        str = line[ 63-no ]
                        num = int(str, 16)
                        result.append( num >> 0 & 1 )
                        result.append( num >> 1 & 1 )
                        result.append( num >> 2 & 1 )
                        result.append( num >> 3 & 1 )
                
                now += 32
                if len(result) >= size:
                    # if we get enough result, break the loop
                    break

    # get size of element in result as final result
    result = result[:size]
    
    # update start
    if ebyte == 0.1:
        ebyte = 1
        # start's unit is byte and bits save in byte, so start plus enough bytes
        if size % 8 != 0:
            start += size // 8 + 1
        else:
            start += size / 8
    else:
        # start plus size of the ebyte
        start += size * ebyte 
         
    # make data into a np.ndarray and same dtype and shape with golden
    data = np.array(result, dtype='uint%d' % (ebyte*8))
    data.dtype = dtype
    data = data.reshape( golden.shape )

    return data

def check_to_txt(golden, result, filename, check_str):
    a = golden.reshape(-1)
    b = result.reshape(-1)
    ah = a.copy()
    ah.dtype = f'uint{a.itemsize * 8}'
    bh = b.copy()
    bh.dtype = f'uint{b.itemsize * 8}'

    w = a.itemsize * 2
    if a.dtype == np.float16 or a.dtype == np.float32 or a.dtype == np.float64 or a.dtype == jnp.bfloat16:
        t = 'f'
    else:
        t = 'd'

    check_result = True
    with open(filename, 'w') as file:
        print( f'         %{2*w+12}s  %{2*w+12}s' % ( 'golden', 'result' ), file=file)
        for i in range(a.shape[0]):
            golden = a[i]
            result = b[i]
            if eval(check_str):
                print(f'%8d: %{w+10}{t}(%0{w}x), %{w+10}{t}(%0{w}x)' % (i, a[i], ah[i], b[i], bh[i]), file=file)
            else:
                print(f'%8d: %{w+10}{t}(%0{w}x), %{w+10}{t}(%0{w}x), mismatch' % (i, a[i], ah[i], b[i], bh[i]), file=file)
                check_result = False
    
    return check_result

def copy_to_dtype( input, dtype ):
    output = input.copy()
    if output.shape == ():
        output = output.reshape(1,)
    output.dtype = dtype
    return output

def main():
    golden_file = sys.argv[1]
    iss_sig_file = sys.argv[2]
    readelf_path = sys.argv[3]

    readelf_cmd = readelf_path + ' -s test.elf'


    try:
        addr_begin_sig_str =  str( subprocess.check_output( readelf_cmd + ' | grep begin_signature ', shell=True ), encoding = 'utf-8' )
        addr_begin_sig = int( addr_begin_sig_str.split()[1], 16 )
    except:
        print("we can't use readelf to find begin_signature from elf, please check.")
        sys.exit(-1)
        

    # get the cases list in the case, including test_num, name, check string, golden
    case_list = np.load( golden_file, allow_pickle=True )
    result_info_list = []
    for test_case in case_list:
        if test_case["check_str"] != '':
            # when test["check_str"] == 0, no need to check
            try:
                addr_testdata_str =  str( subprocess.check_output( readelf_cmd + f' | grep test_{test_case["no"]}_data ', shell=True ), encoding = 'utf-8' )
                addr_testdata = int( addr_testdata_str.split()[1], 16 )
            except:
                print( f"Can't find symbol test_{test_case['no']}_data, please check test.map.\n" )
                continue

            golden = copy_to_dtype( test_case["golden_data"], eval(f'jnp.{test_case["golden_dtype"]}') )

            #because many subcases in one signature file, so we need the spike_start to know where to find the result
            result = from_txt( iss_sig_file, golden,  addr_testdata - addr_begin_sig )
            result_info = { "name":test_case["name"], 'no':test_case['no'], "start_addr":addr_testdata - addr_begin_sig, 
            "spike_result_data":copy_to_dtype(result, np.uint8), "spike_result_dtype":str(result.dtype)}
            result_info_list.append( result_info )

            #save the python golden result and spike result into check.data file of each case        
            check_result = check_to_txt( golden, result, 'check.data', test_case["check_str"] )
            if not check_result:
                print(f'The python golden data and spike results of test case {test_case["no"]} in test.S check failed. You can find the data in check.data\n')

    np.save("spike.npy", result_info_list)
    print("check done.")
     
if __name__ == "__main__":
    main()
