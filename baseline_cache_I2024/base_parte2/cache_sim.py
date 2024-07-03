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

        # Se imprimen las estadísticas de uso y se crea el archivo de destino 
        results = l1_cache.print_stats()
        # Si se solicitó el L2, se crea este
        if options.has_l2:
            results.append(l2_cache.print_stats())
        # Si se solicitó el L3, se crea este
        if options.has_l3:
            results.append(l3_cache.print_stats())
        trace_name = str(options.TRACE_FILE)
        trace_name = str(trace_name).replace("../../traces/", "") 
        results = trace_name + ', ' + str(results)
        results = results.replace("[", "")
        results = results.replace("]", "")
        print()
        print(results)
#        set_trace()
#        results_file_name = str(trace_name +
#                             "L1_cfg_" + options.l1_s + "_" + options.l1_a + "-" +
#                             "L2_cfg" + options.has_l2 + "_" + options.l2_s + "_" + options.l2_a + "__" +
#                             "L3_cfg_" + options.has_l3 + "_" + options.l3_s + "_" + options.l3_a +
#                             "__" + "Block_size" + options.block_size + ".csv")
#        archivo_guardado = open(results_file_name, "w")
#        archivo_guardado.write(results)
#        archivo_guardado.close()





























