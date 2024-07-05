from optparse import OptionParser
import gzip
from cache import *

parser = OptionParser()
parser.add_option("-s", dest="cache_capacity")
parser.add_option("-a", dest="cache_assoc")
parser.add_option("-b", dest="block_size")
parser.add_option("-r", dest="repl_policy")
parser.add_option("-t", dest="TRACE_FILE")

(options, args) = parser.parse_args()

cache = cache(options.cache_capacity, options.cache_assoc, options.block_size, options.repl_policy)

i = 0 #SOLO PARA DEBUG
with gzip.open(options.TRACE_FILE,'rt') as trace_fh:
    for line in trace_fh:
        line = line.rstrip()
        access_type, hex_str_address  = line.split(" ")
        address = int(hex_str_address, 16)
        cache.access(access_type, address)

# Variable para remover ubicación
dir_source = "/home/juan/UCR/tarea4_IE0521/traces/"

# Se salvan los datos en disco para procesarlos después
encabezado = ["cache_capacity",
              "cache_assoc",
              "block_size",
              "repl_policy",
              "TRACE_FILE",
              "total_misses",
              "miss_rate"]
results = [options.cache_capacity,
           options.cache_assoc,
           options.block_size,
           options.repl_policy,
           options.TRACE_FILE.replace(dir_source,"")]
results.append(cache.print_stats())
results = str(results)
results = results.replace("[", "")
results = results.replace("]", "")
results = results.replace("'", "")
encabezado = str(encabezado) + "\n"
encabezado = encabezado.replace("[", "")
encabezado = encabezado.replace("]", "")
encabezado = encabezado.replace("'", "")
file_name = "Sim_Cache_-s_{0}_-a_{1}_-b_{2}_-r_{3}_-t_{4}.csv".format(options.cache_capacity,
                                                                  options.cache_assoc,
                                                                  options.block_size,
                                                                  options.repl_policy,
                                                                  options.TRACE_FILE.replace(dir_source,""))

archivo = open(file_name, "w")
archivo.write(encabezado)
archivo.write(results)
archivo.close()

