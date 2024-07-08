#!/usr/bin/python3

'''
Este script ejecuta y salva las pruebas de la parte 2 de champsim de la 
tarea 4 de IE0521
'''
# Bibliotecas
import time
import datetime
from os import system, getcwd, chdir, listdir
from pdb import set_trace

dir_actual = getcwd()

# Funciones
def sim_cache_parameters(Traces, config_original, dir_sim_p2, archivo_config, dir_Traces, dir_resultados, cmd_sim):
    # Valores a iterar
    cache_capacities = [8, 16, 32, 64, 128]
    cache_assocs = [1, 2, 4, 8, 16]
    block_sizes = [16, 32, 64, 128]
    repl_policies = ['l', 'r']
    cache_level = [1,2,3]

    for capacity in cache_capacities:
        for assoc in cache_assocs:
            for block_size in block_sizes:
                for policy in repl_policies:
                    print(f"\tINFO: Modificando parametros cache_capacity = {capacity}, cache_assoc = {assoc}, block_size = {block_size}, repl_policy = {policy}")
                    # Se empieza por configurar el simulador
                    chdir(dir_sim_p2) # Se va al directorio de champsim para editar cfg
                    config_tmp = config_original
                    config_tmp['cache']['capacity'] = capacity
                    config_tmp['cache']['associativity'] = assoc
                    config_tmp['cache']['block_size'] = block_size
                    config_tmp['cache']['replacement_policy'] = policy
                    config_tmp['cache']['cache_level'] = cache_level

                    # A partir de aca inicia la simulacion
                    for j in Traces:
                        print(f"\t\tINFO: Simulando cache_capacity = {capacity}, cache_assoc = {assoc}, block_size = {block_size}, repl_policy = {policy}, trace = {j}")
                        chdir(dir_Traces)
                        # Nombre de resultados y comando de ejecucion
                        nombre_dest = f"Sim_res_cache_capacity_{capacity}_assoc_{assoc}_block_size_{block_size}_policy_{policy}_trace_{j}.txt"
                        cmd_sim_tmp = dir_sim_p2 + "bin/"+ cmd_sim + j + " > " + nombre_dest
                        # Se ejecuta la simulacion
#                        system(cmd_sim_tmp)


def sim_cache_L1(Traces, dir_sim_p2, dir_Traces, dir_res_L1):
    # Valores a iterar
    #cache_capacity = 32
    #cache_assoc = 8
    #block_size = 64
    #repl_policy = 'l'
    #cache_level = 1

    l1_cap = 32
    l1_assoc = 8
    #l2_caps = [64,128]
    #l2_assocs = [8,16]
    #l3_cap = 
    #l3_asso = 
    block_size = 64
    repl_policy = 'l'

    contador_PG = 0
    contador_TF = 0
    #max_PG = cache_capacities
    max_TF = len(Traces)

    #for cache_capacity in cache_capacities:
    print(f"\tINFO: Experimento 1 - Caché de un único nivel")
    #print("\tProgreso CC: ", contador_PG, "/", max_PG)
    # Se va al directorio para simular
    chdir(dir_res_L1)
    contador_TF = 0

    # A partir de aca inicia la simulacion
    for trace_file in Traces:
        print(f"\t\tINFO: Simulando cache_capacity = {l1_cap}, cache_assoc = {l1_cap}, block_size = {block_size}, repl_policy = {repl_policy}, trace = {trace_file}")
        print("\t\tProgreso Traces: ", contador_TF, "/", max_TF)
        # Trace file 
        trace_file = dir_Traces + trace_file
        # Nombre de resultados y comando de ejecucion
        cmd_sim = f'python3 {dir_sim_p2} --l1_s "{l1_cap}" --l1_a "{l1_assoc}" -b "{block_size}" -t "{trace_file}"'
        # Se ejecuta la simulacion
        system(cmd_sim)
        contador_TF += 1
        contador_PG += 1


def sim_cache_L2(Traces, dir_sim_p2, dir_Traces, dir_res_L2):
    # Valores a iterar
    #cache_capacities = [64,128]
    #cache_assocs = [8, 16]
    #block_size = 64
    #repl_policy = 'l'
    #cache_level = 2

    l1_cap = 32
    l1_assoc = 8
    l2_caps = [64,128]
    l2_assocs = [8,16]
    #l3_cap = 
    #l3_asso = 
    block_size = 64
    repl_policy = 'l'

    # Esto es lo que hay de declarar, hay una: la que se va a ciclar que no se declara, sino que se pone un vector de posibilidades.
    #l1_cap =  
    #l1_assoc = 
    #l2_cap = 
    #l2_assoc = 
    #l3_cap = 
    #l3_asso = 
    #block_size = 
    #repl_policy = 

    contador_PG = 0 # Cont Proceso general
    contador_PG2 = 0 # Cont Proceso general2
    contador_TF = 0 # Cont Trace Files
    max_PG = len(l2_caps)
    max_PG2 = len(l2_assocs)
    max_TF = len(Traces)

    #para cambiar la capacidad del caché
    for l2_cap in l2_caps:
        print(f"\tINFO: Experimento 2 - Segundo nivel de cache: Capacidad de cachés")
        print("\tProgreso CC: ", contador_PG, "/", max_PG)
        # Se va al directorio para simular
        chdir(dir_res_L2)
        contador_TF = 0

        #para cambiar la asociatividad del caché
        for l2_assoc in l2_assocs:
            print(f"\tINFO: Experimento 2 - Segundo nivel de caché: Asociatividad de cachés")
            print("\tProgreso general: ", contador_PG2, "/", max_PG)
            # Se va al directorio para simular
            contador_TF = 0

            # A partir de aca inicia la simulacion
            for trace_file in Traces:
                # TODO 's:
                #   Copiar todos los prints de estado y los cmd_sim al resto de los experimentos
                #   Configurar las variables de modo que existan las que vienen entre los curly brackets
                # antes de que llegue al ciclo -> todas las vairbles tiene que estar declaradas antes de que 
                # empiece el experimento
                #   Confiruar un experimento por función: en cada experimento se itera sobre una variable: así,
                # se tiene un vector con nombre en plural y en el for se tiene el nombre en singular: l1_cache_assocs
                # es un vector y l1_cache_assoc se define en el for
                #   Probar, debuggear y dejar subido en git
                print(f"\t\tINFO: Simulando --l1_s {l1_cap} --l1_a {l1_assoc} --l2_s {l2_cap} --l2_a {l2_assoc} --l2 -b {block_size} -t {trace_file}")
                print("\t\tProgreso Traces: ", contador_TF, "/", max_TF)
                # Trace file 
                trace_file = dir_Traces + trace_file
                # Nombre de resultados y comando de ejecucion
                cmd_sim = f'python3 {dir_sim_p2} --l1_s "{l1_cap}" --l1_a "{l1_assoc}" --l2_s "{l2_cap}" --l2_a "{l2_assoc}" --l2 -b "{block_size}" -t "{trace_file}"'
    
                # Se ejecuta la simulacion
                system(cmd_sim)
                contador_TF += 1
            contador_PG2 += 1
        contador_PG += 1


def sim_cache_L3(Traces, dir_sim_p2, dir_Traces, dir_res_L3):
    # Valores a iterar
    #cache_capacities = [512, 1024]
    #cache_assocs = [16, 32]
    #block_size = 64
    #repl_policy = 'l'
    #cache_level = 3

    l1_cap =  32
    l1_assoc = 8
    l2_cap = 256
    l2_assoc = 8
    l3_caps = [512, 1024]
    l3_assocs = [16,32]
    block_size = 64
    repl_policy = 'l'

    contador_PG = 0 # Cont Proceso general
    contador_PG2 = 0 # Cont Proceso general2
    contador_TF = 0 # Cont Trace Files
    max_PG = len(l3_assocs)
    max_PG2 = len(l3_caps)
    max_TF = len(Traces)

       #para cambiar la capacidad del caché
    for l3_cap in l3_caps:
        print(f"\tINFO: Experimento 3 - Tercer nivel de cache")
        print("\tProgreso CC: ", contador_PG, "/", max_PG)
        # Se va al directorio para simular
        chdir(dir_res_L3)
        contador_TF = 0

        #para cambiar la asociatividad del caché
        for l3_assoc in l3_assocs:
            print(f"\tINFO: Experimento 3 - Tercer nivel de cache")
            print("\tProgreso general: ", contador_PG2, "/", max_PG)
            # Se va al directorio para simular
            contador_TF = 0

            # A partir de aca inicia la simulacion
            for trace_file in Traces:
                print(f"\t\tINFO: Simulando --l1_s {l1_cap} --l1_a {l1_assoc} --l2_s {l2_cap} --l2_a {l2_assoc} --l3_s {l3_cap} --l3_a {l3_assoc} --l2 --l3 -b {block_size} -t {trace_file}")
                print("\t\tProgreso Traces: ", contador_TF, "/", max_TF)
                # Trace file 
                trace_file = dir_Traces + trace_file
                # Nombre de resultados y comando de ejecucion
                cmd_sim = f'python3 {dir_sim_p2}  --l1_s "{l1_cap}" --l1_a "{l1_assoc}" --l2_s "{l2_cap}" --l2_a "{l2_assoc}" --l3_s "{l3_cap}" --l3_a "{l3_assoc}" --l2 --l3 -b "{block_size}" -t "{trace_file}"'
                # Se ejecuta la simulacion
                system(cmd_sim)
                contador_TF += 1
            contador_PG2 += 1
        contador_PG += 1



# Declaracion de variables
dir_sim_p2     = dir_actual + "/baseline_cache_I2024/base_parte2/cache_sim.py"
dir_Traces     = dir_actual + "/traces/"
dir_res_L1     = dir_actual + "/Results/Part2/Cache_L1/"
dir_res_L2     = dir_actual + "/Results/Part2/Cache_L2/"
dir_res_L3     = dir_actual + "/Results/Part2/Cache_L3/"
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
print("t_1/1. Inicio. ", "{:%Y-%b-%d %H:%M:%S}".format(datetime.datetime.now()))
print()
sim_cache_L1(Traces, dir_sim_p2, dir_Traces, dir_res_L1)

t_1 = time.time()
print("t_2/3. Inicio. ", "{:%Y-%b-%d %H:%M:%S}".format(datetime.datetime.now()))
print("\tTiempo utilizado en tarea t_1: ", t_1 - t_0)
print()
sim_cache_L2(Traces, dir_sim_p2, dir_Traces, dir_res_L2)

t_2 = time.time()
print("t_3/3. Inicio. ", "{:%Y-%b-%d %H:%M:%S}".format(datetime.datetime.now()))
print("\tTiempo utilizado en tarea t_2: ", t_2 - t_1)
print()
sim_cache_L3(Traces, dir_sim_p2, dir_Traces, dir_res_L3)

t_3 = time.time()
print("\tTiempo utilizado en tarea t_3: ", t_3 - t_2)
print()
print("\tTiempo total: ", t_3 - t_0)

set_trace()
