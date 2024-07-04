#!/usr/bin/python3
# Se encarga de llevar a cabo las simulación
'''
Este script se encarga de ejecutar y salvar las pruebas de champsim de la
tarea 3 de IE0521.
'''
# Bibliotecas
import cache
import cache_sim
import time
import datetime
from os import system, getcwd, chdir, listdir
from pdb import set_trace

# Funciones
def obtener_orig_cfg(dir_champsim, archivo_config):
    # Leer la configuracion original del directorio de champsim
    chdir(dir_champsim) # Se va al directorio de champsim para editar cfg
    system("rm champsim_config.json")
    system("cp champsim_config.json.bak champsim_config.json")
    archivo_cfg = open((dir_champsim + archivo_config), 'r')
    config = json.load(archivo_cfg)
    archivo_cfg.close()
    return config


def sim_cache_parameters(Traces, config_original, dir_champsim, archivo_config, dir_Traces, dir_resultados, cmd_sim):
    # Valores a iterar
    cache_capacities = [8, 16, 32, 64, 128]
    cache_assocs = [1, 2, 4, 8, 16]
    block_sizes = [16, 32, 64, 128]
    repl_policies = ['LRU', 'random']

    for capacity in cache_capacities:
        for assoc in cache_assocs:
            for block_size in block_sizes:
                for policy in repl_policies:
                    print(f"\tINFO: Modificando parametros cache_capacity = {capacity}, cache_assoc = {assoc}, block_size = {block_size}, repl_policy = {policy}")
                    # Se empieza por configurar el simulador
                    chdir(dir_champsim) # Se va al directorio de champsim para editar cfg
                    config_tmp = config_original
                    config_tmp['cache']['capacity'] = capacity
                    config_tmp['cache']['associativity'] = assoc
                    config_tmp['cache']['block_size'] = block_size
                    config_tmp['cache']['replacement_policy'] = policy
                    archivo_cfg = open(archivo_config, "w")     # Se salva la configuracion
                    json.dump(config_tmp, archivo_cfg)          # al archivo
                    archivo_cfg.close()
                    system(("./config.sh " + archivo_config))   # Se recupera la cfg orig
                    system("make -j 6")                              # Se recompila el simulador

                    # A partir de aca inicia la simulacion
                    for j in Traces:
                        print(f"\t\tINFO: Simulando cache_capacity = {capacity}, cache_assoc = {assoc}, block_size = {block_size}, repl_policy = {policy}, trace = {j}")
                        chdir(dir_Traces)
                        # Nombre de resultados y comando de ejecucion
                        nombre_dest = f"Sim_res_cache_capacity_{capacity}_assoc_{assoc}_block_size_{block_size}_policy_{policy}_trace_{j}.txt"
                        cmd_sim_tmp = dir_champsim + "bin/"+ cmd_sim + j + " > " + nombre_dest
                        # Se ejecuta la simulacion
                        system(cmd_sim_tmp)


def restaurar_cfg(dir_champsim, archivo_config, config_original):
    # Se restaura la configuracion original
    chdir(dir_champsim) # Se va al directorio de champsim para editar cfg
    system("rm champsim_config.json")
    system("cp champsim_config.json.bak champsim_config.json")


# Declaracion de variables
cmd_sim = "champsim --warmup_instructions 10000000 --simulation_instructions 100000000 "
archivo_config = "champsim_config.json"
dir_resultados = "/home/juan/UCR/Semestres/I S, 2024/IE0521 - Estructuras de computadoras digitales II/Tareas/tarea_3/Resultados/"
dir_champsim = "/home/juan/Archivos/Software/ChampSim/"
dir_Traces = "/home/juan/UCR/Semestres/I S, 2024/IE0521 - Estructuras de computadoras digitales II/Tareas/Traces/"
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
global config_original
config_original = obtener_orig_cfg(dir_champsim, archivo_config)

t_0 = time.time()
print("t_1/4. Inicio. ", "{:%Y-%b-%d %H:%M:%S}".format(datetime.datetime.now()))
print()
sim_cache_parameters(Traces, config_original, dir_champsim, archivo_config, dir_Traces, dir_resultados, cmd_sim)
restaurar_cfg(dir_champsim, archivo_config, config_original)

t_1 = time.time()
print("t_2/4. Inicio. ", "{:%Y-%b-%d %H:%M:%S}".format(datetime.datetime.now()))
print("\tTiempo utilizado en tarea t_1: ", t_1 - t_0)
print()

config_original = obtener_orig_cfg(dir_champsim, archivo_config)
# No es necesario llamar a otras funciones de simulación ya que estamos centrados en los parámetros de caché
restaurar_cfg(dir_champsim, archivo_config, config_original)

t_2 = time.time()
print("t_3/4. Inicio. ", "{:%Y-%b-%d %H:%M:%S}".format(datetime.datetime.now()))
print("\tTiempo utilizado en tarea t_2: ", t_2 - t_1)
print()

t_3 = time.time()
print("t_4/4. Inicio. ", "{:%Y-%b-%d %H:%M:%S}".format(datetime.datetime.now()))
print("\tTiempo utilizado en tarea t_3: ", t_3 - t_2)
print()

t_4 = time.time()
print("\tTiempo utilizado en tarea t_4: ", t_4 - t_3)
print()
print("\tTiempo total: ", t_4 - t_0)

set_trace()