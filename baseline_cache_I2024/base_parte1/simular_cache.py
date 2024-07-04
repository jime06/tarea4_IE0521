#!/usr/bin/python3
# Se encarga de llevar a cabo las simulación
'''
Este script se encarga de ejecutar y salvar las pruebas de champsim de la
tarea 4 de IE0521.
'''
# Bibliotecas
import time
import datetime
from os import system, getcwd, chdir, listdir
from pdb import set_trace

# Funciones
def sim_cache_parameters(Traces, config_original, dir_sim_p1, archivo_config, dir_Traces, dir_resultados, cmd_sim):
    # Valores a iterar
    cache_capacities = [8, 16, 32, 64, 128]
    cache_assocs = [1, 2, 4, 8, 16]
    block_sizes = [16, 32, 64, 128]
    repl_policies = ['l', 'r']
    reference_values = []

    for capacity in cache_capacities:
        for assoc in cache_assocs:
            for block_size in block_sizes:
                for policy in repl_policies:
                    print(f"\tINFO: Modificando parametros cache_capacity = {capacity}, cache_assoc = {assoc}, block_size = {block_size}, repl_policy = {policy}")
                    # Se empieza por configurar el simulador
                    chdir(dir_sim_p1) # Se va al directorio de champsim para editar cfg
                    config_tmp = config_original
                    config_tmp['cache']['capacity'] = capacity
                    config_tmp['cache']['associativity'] = assoc
                    config_tmp['cache']['block_size'] = block_size
                    config_tmp['cache']['replacement_policy'] = policy

                    # A partir de aca inicia la simulacion
                    for j in Traces:
                        print(f"\t\tINFO: Simulando cache_capacity = {capacity}, cache_assoc = {assoc}, block_size = {block_size}, repl_policy = {policy}, trace = {j}")
                        chdir(dir_Traces)
                        # Nombre de resultados y comando de ejecucion
                        nombre_dest = f"Sim_res_cache_capacity_{capacity}_assoc_{assoc}_block_size_{block_size}_policy_{policy}_trace_{j}.txt"
                        cmd_sim_tmp = dir_sim_p1 + "bin/"+ cmd_sim + j + " > " + nombre_dest
                        # Se ejecuta la simulacion
                        system(cmd_sim_tmp)


def sim_cache_size(Traces, dir_sim_p1, dir_Traces, dir_resultados):
    # Valores a iterar
    cache_capacities = [8, 16, 32, 64, 128]
    cache_assoc = 8
    block_size = 64
    repl_policy = 'l'

    contador_PG = 0
    contador_TF = 0
    max_PG = len(cache_capacities)
    max_TF = len(Traces)

    for cache_capacity in cache_capacities:
        print(f"\tINFO: Experimento 1 - Tamaño de la caché")
        print("\tProgreso CC: ", contador_PG, "/", max_PG)
        # Se va al directorio para simular
        chdir(dir_resultados)

        # A partir de aca inicia la simulacion
        for trace_file in Traces:
            print(f"\t\tINFO: Simulando cache_capacity = {cache_capacity}, cache_assoc = {cache_assoc}, block_size = {block_size}, repl_policy = {repl_policy}, trace = {trace_file}")
            print("\t\tProgreso Traces: ", contador_TF, "/", max_TF)
            # Trace file 
            trace_file = dir_Traces + trace_file
            # Nombre de resultados y comando de ejecucion
            cmd_sim = f'python3 {dir_sim_p1} -s "{cache_capacity}" -a "{cache_assoc}" -b "{block_size}" -r "{repl_policy}" -t "{trace_file}"'
            # Se ejecuta la simulacion
            system(cmd_sim)
            contador_TF += 1
        contador_PG += 1


def sim_cache_assoc(Traces, dir_sim_p1, dir_Traces, dir_resultados):
    # Valores a iterar
    cache_capacity = 32
    cache_assocs = [1, 2, 4, 8, 16]
    block_size = 64
    repl_policy = 'l'

    contador_PG = 0 # Cont Proceso general
    contador_TF = 0 # Cont Trace Files
    max_PG = len(cache_assocs)
    max_TF = len(Traces)

    for cache_assoc in cache_assocs:
        print(f"\tINFO: Experimento 2 - Asociatividad de la Caché")
        print("\tProgreso general: ", contador_PG, "/", max_PG)
        # Se va al directorio para simular
        chdir(dir_resultados)

        # A partir de aca inicia la simulacion
        for trace_file in Traces:
            print(f"\t\tINFO: Simulando cache_assoc = {cache_capacity}, cache_assoc = {cache_assoc}, block_size = {block_size}, repl_policy = {repl_policy}, trace = {trace_file}")
            print("\t\tProgreso Traces: ", contador_TF, "/", max_TF)
            # Trace file 
            trace_file = dir_Traces + trace_file
            # Nombre de resultados y comando de ejecucion
            cmd_sim = f'python3 {dir_sim_p1} -s "{cache_capacity}" -a "{cache_assoc}" -b "{block_size}" -r "{repl_policy}" -t "{trace_file}"'
            # Se ejecuta la simulacion
            system(cmd_sim)
            contador_TF += 1
        contador_PG += 1


def sim_cache_block_size(Traces, dir_sim_p1, dir_Traces, dir_resultados):
    # Valores a iterar
    cache_capacity = 32
    cache_assoc = 8
    block_sizes = [16, 32, 64, 128]
    repl_policy = 'l'

    contador_PG = 0 # Cont Proceso general
    contador_TF = 0 # Cont Trace Files
    max_PG = len(block_sizes)
    max_TF = len(Traces)

    for block_size in block_sizes:
        print(f"\tINFO: Experimento 2 - Tamaño del bloque de la caché")
        print("\tProgreso general: ", contador_PG, "/", max_PG)
        # Se va al directorio para simular
        chdir(dir_resultados)

        # A partir de aca inicia la simulacion
        for trace_file in Traces:
            print(f"\t\tINFO: Simulando block_size = {cache_capacity}, cache_assoc = {cache_assoc}, block_size = {block_size}, repl_policy = {repl_policy}, trace = {trace_file}")
            print("\t\tProgreso Traces: ", contador_TF, "/", max_TF)
            # Trace file 
            trace_file = dir_Traces + trace_file
            # Nombre de resultados y comando de ejecucion
            cmd_sim = f'python3 {dir_sim_p1} -s "{cache_capacity}" -a "{cache_assoc}" -b "{block_size}" -r "{repl_policy}" -t "{trace_file}"'
            # Se ejecuta la simulacion
            system(cmd_sim)
            contador_TF += 1
        contador_PG += 1


def sim_cache_replacement_policy(Traces, dir_sim_p1, dir_Traces, dir_resultados):
    # Valores a iterar
    cache_capacity = 32
    cache_assoc = 8
    block_size = 64
    repl_policies = ['l', 'r']

    contador_PG = 0 # Cont Proceso general
    contador_TF = 0 # Cont Trace Files
    max_PG = len(repl_policies)
    max_TF = len(Traces)

    for repl_policy in repl_policies:
        print(f"\tINFO: Experimento 4 - Política de reemplazo del caché")
        print("\tProgreso general: ", contador_PG, "/", max_PG)
        # Se va al directorio para simular
        chdir(dir_resultados)

        # A partir de aca inicia la simulacion
        for trace_file in Traces:
            print(f"\t\tINFO: Simulando block_size = {cache_capacity}, cache_assoc = {cache_assoc}, block_size = {block_size}, repl_policy = {repl_policy}, trace = {trace_file}")
            print("\t\tProgreso Traces: ", contador_TF, "/", max_TF)
            # Trace file 
            trace_file = dir_Traces + trace_file
            # Nombre de resultados y comando de ejecucion
            cmd_sim = f'python3 {dir_sim_p1} -s "{cache_capacity}" -a "{cache_assoc}" -b "{block_size}" -r "{repl_policy}" -t "{trace_file}"'
            # Se ejecuta la simulacion
            system(cmd_sim)
            contador_TF += 1
        contador_PG += 1


# Declaracion de variables
dir_sim_p1     = "/home/juan/UCR/tarea4_IE0521/baseline_cache_I2024/base_parte1/cache_sim.py"
dir_Traces     = "/home/juan/UCR/tarea4_IE0521/traces/"
dir_res_CS     = "/home/juan/UCR/tarea4_IE0521/Results/Part1/Cache_Size/"
dir_res_CA     = "/home/juan/UCR/tarea4_IE0521/Results/Part1/Cache_Assoc/"
dir_res_CB     = "/home/juan/UCR/tarea4_IE0521/Results/Part1/Cache_Block/"
dir_res_CR     = "/home/juan/UCR/tarea4_IE0521/Results/Part1/Cache_Replacement/"
Traces = ["400.perlbench-41B.trace.txt.gz",
            "401.bzip2-226B.trace.txt.gz",
            "403.gcc-16B.trace.txt.gz",
            "410.bwaves-1963B.trace.txt.gz",
            "416.gamess-875B.trace.txt.gz",
            "429.mcf-184B.trace.txt.gz",
            "433.milc-127B.trace.txt.gz",
            "435.gromacs-111B.trace.txt.gz",
            "436.cactusADM-1804B.trace.txt.gz",
            "437.leslie3d-134B.trace.txt.gz",
            "444.namd-120B.trace.txt.gz",
            "445.gobmk-17B.trace.txt.gz",
            "450.soplex-247B.trace.txt.gz",
            "453.povray-887B.trace.txt.gz",
            "454.calculix-104B.trace.txt.gz",
            "456.hmmer-191B.trace.txt.gz",
            "458.sjeng-1088B.trace.txt.gz",
            "459.GemsFDTD-1169B.trace.txt.gz",
            "462.libquantum-1343B.trace.txt.gz",
            "464.h264ref-30B.trace.txt.gz",
            "465.tonto-1769B.trace.txt.gz",
            "470.lbm-1274B.trace.txt.gz",
            "471.omnetpp-188B.trace.txt.gz",
            "473.astar-153B.trace.txt.gz",
            "481.wrf-1170B.trace.txt.gz",
            "482.sphinx3-1100B.trace.txt.gz",
            "483.xalancbmk-127B.trace.txt.gz"]

# Inicio del programa
t_0 = time.time()
print("t_1/4. Inicio. ", "{:%Y-%b-%d %H:%M:%S}".format(datetime.datetime.now()))
print()
sim_cache_size(Traces, dir_sim_p1, dir_Traces, dir_res_CS)

t_1 = time.time()
print("t_2/4. Inicio. ", "{:%Y-%b-%d %H:%M:%S}".format(datetime.datetime.now()))
print("\tTiempo utilizado en tarea t_1: ", t_1 - t_0)
print()
sim_cache_assoc(Traces, dir_sim_p1, dir_Traces, dir_res_CA)

t_2 = time.time()
print("t_3/4. Inicio. ", "{:%Y-%b-%d %H:%M:%S}".format(datetime.datetime.now()))
print("\tTiempo utilizado en tarea t_2: ", t_2 - t_1)
print()
sim_cache_block_size(Traces, dir_sim_p1, dir_Traces, dir_res_CB)

t_3 = time.time()
print("t_4/4. Inicio. ", "{:%Y-%b-%d %H:%M:%S}".format(datetime.datetime.now()))
print("\tTiempo utilizado en tarea t_3: ", t_3 - t_2)
print()
sim_cache_replacement_policy(Traces, dir_sim_p1, dir_Traces, dir_res_CR)

t_4 = time.time()
print("\tTiempo utilizado en tarea t_4: ", t_4 - t_3)
print()
print("\tTiempo total: ", t_4 - t_0)

set_trace()
