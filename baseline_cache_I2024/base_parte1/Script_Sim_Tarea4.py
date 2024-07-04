#!/usr/bin/python3
'''
Este script se encarga de ejecutar y salvar las pruebas de champsim de la
tarea 3 de IE0521.
'''
# Bibliotecas
import json
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


def sim_rob_size(Traces, config_original, dir_champsim, archivo_config, dir_Traces, dir_resultados, cmd_sim):
    # Se encarga de realizar las simuaciones del cambio de rob_size
    valores_it = [16, 64, 352, 512]
    # Se itera sobre los valores a estudiar para configurar y simular todo
    config_tmp = config_original
    for i in valores_it:
        print("\tINFO: Modificando parametro rob_size = ", i)
        # Se empieza por configurar el simulador
        chdir(dir_champsim) # Se va al directorio de champsim para editar cfg
        config_tmp['ooo_cpu'][0]['rob_size'] = i    # Se cambia el parametro en cuestion
        archivo_cfg = open(archivo_config, "w")     # Se salva la configuracion
        json.dump(config_tmp, archivo_cfg)          # al archivo
        archivo_cfg.close()
        system(("./config.sh " + archivo_config))   # Se recupera la cfg orig
        system("make -j 6")                              # Se recompila el simulador

        # A partir de aca inicia la simulacion
        for j in Traces:
            print("\t\tINFO: Simulando rob_size = ", i, ", trace = ", j)
            chdir(dir_Traces)
            # Nombre de resultados y comando de ejecucion
            nombre_dest = "Sim_res_rob_size_" + str(i) + "_trace_" + j + ".txt"
            cmd_sim_tmp = dir_champsim + "bin/"+ cmd_sim + j + " > " + nombre_dest
            # Se ejecuta la simulacion
            system(cmd_sim_tmp)


def sim_pipeline_width(Traces, config_original, dir_champsim, archivo_config, dir_Traces, dir_resultados, cmd_sim):
    # Se encarga de realizar las simuaciones del cambio de pipeline_width
    valores_it = [4, 6, 8]
    # Se itera sobre los valores a estudiar para configurar y simular todo
    config_tmp = config_original
    for i in valores_it:
        print("\tINFO: Modificando parametro pipeline_width = ", i)
        # Se empieza por configurar el simulador
        chdir(dir_champsim) # Se va al directorio de champsim para editar cfg
        # Se cambian todos los parametros indicados
        config_original['ooo_cpu'][0]["fetch_width"] = i
        config_original['ooo_cpu'][0]["decode_width"] = i
        config_original['ooo_cpu'][0]["dispatch_width"] = i
        config_original['ooo_cpu'][0]["execute_width"] = i
        config_original['ooo_cpu'][0]["lq_width"] = i
        config_original['ooo_cpu'][0]["sq_width"] = i
        config_original['ooo_cpu'][0]["retire_width"] = i 
        archivo_cfg = open(archivo_config, "w")     # Se salva la configuracion
        json.dump(config_tmp, archivo_cfg)          # al archivo
        archivo_cfg.close()
        system(("./config.sh " + archivo_config))   # Se recupera la cfg orig
        system("make -j 6")                              # Se recompila el simulador

        # A partir de aca inicia la simulacion
        for j in Traces:
            print("\t\tINFO: Simulando pipeline_width = ", i, ", trace = ", j)
            chdir(dir_Traces)
            # Nombre de resultados y comando de ejecucion
            nombre_dest = "Sim_res_pipeline_width_" + str(i) + "_trace_" + j + ".txt"
            cmd_sim_tmp = dir_champsim + "bin/"+ cmd_sim + j + " > " + nombre_dest
            # Se ejecuta la simulacion
            system(cmd_sim_tmp)


def sim_branch_predictor(Traces, config_original, dir_champsim, archivo_config, dir_Traces, dir_resultados, cmd_sim):
    # Se encarga de realizar las simuaciones del cambio de branch_predictor
    valores_it = ['bimodal', 'gshare', 'perceptron']
    # Se itera sobre los valores a estudiar para configurar y simular todo
    config_tmp = config_original
    for i in valores_it:
        print("\tINFO: Modificando parametro branch_predictor = ", i)
        # Se empieza por configurar el simulador
        chdir(dir_champsim) # Se va al directorio de champsim para editar cfg
        config_original['ooo_cpu'][0]["branch_predictor"] = i    # Se cambia el parametro en cuestion
        archivo_cfg = open(archivo_config, "w")     # Se salva la configuracion
        json.dump(config_tmp, archivo_cfg)          # al archivo
        archivo_cfg.close()
        system(("./config.sh " + archivo_config))   # Se recupera la cfg orig
        system("make -j 6")                              # Se recompila el simulador

        # A partir de aca inicia la simulacion
        for j in Traces:
            print("\t\tINFO: Simulando branch_predictor = ", i, ", trace = ", j)
            chdir(dir_Traces)
            # Nombre de resultados y comando de ejecucion
            nombre_dest = "Sim_res_branch_predictor_" + str(i) + "_trace_" + j + ".txt"
            cmd_sim_tmp = dir_champsim + "bin/"+ cmd_sim + j + " > " + nombre_dest
            # Se ejecuta la simulacion
            system(cmd_sim_tmp)


def sim_L2_prefetcher(Traces, config_original, dir_champsim, archivo_config, dir_Traces, dir_resultados, cmd_sim):
    # Se encarga de realizar las simuaciones del cambio de L2_prefetcher
    valores_it = ['no', 'next_line', 'ip_stride']
    # Se itera sobre los valores a estudiar para configurar y simular todo
    config_tmp = config_original
    for i in valores_it:
        print("\tINFO: Modificando parametro = L2_prefetcher", i)
        # Se empieza por configurar el simulador
        chdir(dir_champsim) # Se va al directorio de champsim para editar cfg
        config_original["L2C"]['prefetcher'] = i    # Se cambia el parametro en cuestion
        archivo_cfg = open(archivo_config, "w")     # Se salva la configuracion
        json.dump(config_tmp, archivo_cfg)          # al archivo
        archivo_cfg.close()
        system(("./config.sh " + archivo_config))   # Se recupera la cfg orig
        system("make -j 6")                              # Se recompila el simulador

        # A partir de aca inicia la simulacion
        for j in Traces:
            print("\t\tINFO: Simulando L2_prefetcher=", i, ", trace ", j)
            chdir(dir_Traces)
            # Nombre de resultados y comando de ejecucion
            nombre_dest = "Sim_res_L2_prefetcher_" + str(i) + "_trace_" + j + ".txt"
            cmd_sim_tmp = dir_champsim + "bin/"+ cmd_sim + j + " > " + nombre_dest
            # Se ejecuta la simulacion
            system(cmd_sim_tmp)



def restaurar_cfg(dir_champsim, archivo_config, config_original):
    # Se restaura la configuracion original
    chdir(dir_champsim) # Se va al directorio de champsim para editar cfg
    system("rm champsim_config.json")
    system("cp champsim_config.json.bak champsim_config.json")






#def sim_pipeline_width(traces, config_original, dir_champsim, archivo_config, dir_Traces, dir_resultados):
#def sim_branch_predictor(traces, config_original, dir_champsim, archivo_config, dir_Traces, dir_resultados):
#def sim_prefetcher(traces, config_original, dir_champsim, archivo_config, dir_Traces, dir_resultados):

# Declaracion de variables
cmd_sim = "champsim --warmup_instructions 10000000 --simulation_instructions 100000000 "
#cmd_sim = "champsim --warmup_instructions 1 --simulation_instructions 1 "
archivo_config = "champsim_config.json"
dir_resultados = "/home/juan/UCR/Semestres/I S, 2024/IE0521 - Estructuras de computadoras digitales II/Tareas/tarea_3/Resultados/"
dir_champsim = "/home/juan/Archivos/Software/ChampSim/"
dir_Traces = "/home/juan/UCR/Semestres/I S, 2024/IE0521 - Estructuras de computadoras digitales II/Tareas/Traces/"
Traces = ["600.perlbench_s-1273B.champsimtrace.xz",
          "605.mcf_s-1152B.champsimtrace.xz",
          "619.lbm_s-2676B.champsimtrace.xz",
          "648.exchange2_s-1227B.champsimtrace.xz",
          "654.roms_s-1007B.champsimtrace.xz"]

# Inicio del programa
global config_original
config_original = obtener_orig_cfg(dir_champsim, archivo_config)

t_0 = time.time()
print("t_1/4. Inicio. ", "{:%Y-%b-%d %H:%M:%S}".format(datetime.datetime.now()))
print()

sim_rob_size(Traces, config_original, dir_champsim, archivo_config, dir_Traces, dir_resultados, cmd_sim)
restaurar_cfg(dir_champsim, archivo_config, config_original)

t_1 = time.time()
print("t_2/4. Inicio. ", "{:%Y-%b-%d %H:%M:%S}".format(datetime.datetime.now()))
print("\tTiempo utilizado en tarea t_1: ", t_1 - t_0)
print()

config_original = obtener_orig_cfg(dir_champsim, archivo_config)
sim_pipeline_width(Traces, config_original, dir_champsim, archivo_config, dir_Traces, dir_resultados, cmd_sim)
restaurar_cfg(dir_champsim, archivo_config, config_original)

t_2 = time.time()
print("t_3/4. Inicio. ", "{:%Y-%b-%d %H:%M:%S}".format(datetime.datetime.now()))
print("\tTiempo utilizado en tarea t_2: ", t_2 - t_1)
print()

config_original = obtener_orig_cfg(dir_champsim, archivo_config)
sim_branch_predictor(Traces, config_original, dir_champsim, archivo_config, dir_Traces, dir_resultados, cmd_sim)
restaurar_cfg(dir_champsim, archivo_config, config_original)

t_3 = time.time()
print("t_4/4. Inicio. ", "{:%Y-%b-%d %H:%M:%S}".format(datetime.datetime.now()))
print("\tTiempo utilizado en tarea t_3: ", t_3 - t_2)
print()

config_original = obtener_orig_cfg(dir_champsim, archivo_config)
sim_L2_prefetcher(Traces, config_original, dir_champsim, archivo_config, dir_Traces, dir_resultados, cmd_sim)
restaurar_cfg(dir_champsim, archivo_config, config_original)

t_4 = time.time()
print("\tTiempo utilizado en tarea t_4: ", t_4 - t_3)
print()
print("\tTiempo total: ", t_4 - t_0)

set_trace()
