from optparse import OptionParser
import gzip
import sys
from cache import *
from pdb import set_trace

parser = OptionParser()
parser.add_option("--l1_s", dest="l1_s")
parser.add_option("--l1_a", dest="l1_a")
parser.add_option("--l2", action="store_true", dest="has_l2")
parser.add_option("--l2_s", dest="l2_s")
parser.add_option("--l2_a", dest="l2_a")
parser.add_option("--l3", action="store_true", dest="has_l3")
parser.add_option("--l3_s", dest="l3_s")
parser.add_option("--l3_a", dest="l3_a")
parser.add_option("-b", dest="block_size", default="64")
parser.add_option("-t", dest="TRACE_FILE")

(options, args) = parser.parse_args()

# Condición de error: se declaró un caché L3 y no L2
if not(options.has_l2) and options.has_l3:
    print("Error: se solicitó un caché L3 y no un L2, no se puede crear caché")
else:
    # Se crea una lista de cachés para recorrerlos
    caches = []

    # El caché L1 siempre se crea
    l1_cache = cache(options.l1_s, options.l1_a, options.block_size, "l", 1)
    caches.append(l1_cache)

    # Si se solicitó el L2, se crea este
    if options.has_l2:
        l2_cache = cache(options.l2_s, options.l2_a, options.block_size, "l", 2)
        caches.append(l2_cache)

    # Si se solicitó el L3, se crea este
    if options.has_l3:
        l3_cache = cache(options.l3_s, options.l3_a, options.block_size, "l", 3)
        caches.append(l3_cache)

    with gzip.open(options.TRACE_FILE,'rt') as trace_fh:
        for line in trace_fh:
            line = line.rstrip()
            access_type, hex_str_address  = line.split(" ")
            address = int(hex_str_address, 16)
            access_results = [] # Se crean los resultados de acceso como
                                # un vector
            for i in range(len(caches)):
                # Se recorren los objtetos de caché para leer los datos
                result_tmp = caches[i].access(access_type, address)
                access_results.append(result_tmp)
            for i in range(len(access_results)):
                # Luego, se determina, con base en si hubo hits o no, si hay que
                # ir a otro caché por el dato  o no
                if (access_results[i] is False):
                    dirs_tmp = caches[i].get_dirs(access_type, address)
                    caches[i].bring_to_cache(dirs_tmp[0], dirs_tmp[1])
                elif (access_results[i] is True):
                    break

# Variable para remover ubicación
dir_source = "/home/juan/UCR/tarea4_IE0521/traces/"

print()

# Se salvan los datos en disco para procesarlos después
encabezado = ["l1_s",
              "l1_a",
              "has_l2",
              "l2_s",
              "l2_a",
              "has_l3",
              "l3_s",
              "l3_a",
              "block_size",
              "TRACE_FILE",
              "l1_misses",
              "l1_miss_rate",
              "l2_misses",
              "l2_miss_rate",
              "l3_misses",
              "l3_miss_rate",
              "AMAT_hacia_l1",
              "AMAT_hacia_l2",
              "AMAT_hacia_l3"
              ]

results = [options.l1_s,
           options.l1_a,
           options.has_l2,
           options.l2_s,
           options.l2_a,
           options.has_l3,
           options.l3_s,
           options.l3_a,
           options.block_size,
           options.TRACE_FILE.replace(dir_source,"")]
# Valores de importancia
ht1 = 4
ht2 = 12
ht3 = 60
mp  = 500


# Se imprimen las estadísticas de uso y se crea el archivo de destino 
cache_res = []
amats = []
cache_res.append(l1_cache.print_stats())
amats.append(((cache_res[0][2] - cache_res[0][0])*ht1 + cache_res[0][1]*mp))

# Si se solicitó el L2, se crea este
if options.has_l2:
    cache_res.append(l2_cache.print_stats()) 
    amats.append(((cache_res[0][2] - cache_res[0][0])*ht1 + cache_res[0][1]*((cache_res[1][2] - cache_res[1][0])*ht1 + cache_res[1][1]*mp)))
else:
    cache_res.append(0) 
    amats.append(0)
# Si se solicitó el L3, se crea este
if options.has_l3:
    cache_res.append(l3_cache.print_stats())
    amats.append(((cache_res[0][2] - cache_res[0][0])*ht1 + cache_res[0][1]*((cache_res[1][2] - cache_res[1][0])*ht2 + cache_res[1][1]*((cache_res[2][2] - cache_res[2][0])*ht3 + cache_res[2][1]*mp))))
else:
    cache_res.append(0) 
    amats.append(0)

cache_res[0].pop(2)
if options.has_l2:
    cache_res[1].pop(2)
if options.has_l3:
    cache_res[2].pop(2)

print()
results.append(cache_res)
results.append(amats)
trace_name = str(options.TRACE_FILE)
trace_name = str(trace_name).replace("../../traces/", "") 
results = str(results)
results = results.replace("[", "")
results = results.replace("]", "")

encabezado = str(encabezado) + "\n"
encabezado = encabezado.replace("[", "")
encabezado = encabezado.replace("]", "")
encabezado = encabezado.replace("'", "")
file_name = "Sim_Cache_-l1_s_{0}__-l1_a_{1}__-has_l2_{2}__-l2_s_{3}__-l2_a_{4}__-has_l3_{5}__-l3_s_{6}__-l3_a_{7}__-block_size_{8}__-trace_file_{9}.csv".format(options.l1_s,
           options.l1_a,
           options.has_l2,
           options.l2_s,
           options.l2_a,
           options.has_l3,
           options.l3_s,
           options.l3_a,
           options.block_size,
           options.TRACE_FILE.replace(dir_source,""))

archivo = open(file_name, "w")
archivo.write(encabezado)
archivo.write(results)
archivo.close()





























