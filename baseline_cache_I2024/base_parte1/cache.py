from math import log2, floor
from random import randint
from pdb import set_trace

class cache:
    def __init__(self, cache_capacity, cache_assoc, block_size, repl_policy):
        #Escriba aquí el init de la clase
        self.total_access = 0
        self.total_misses = 0

        self.cache_capacity = int(cache_capacity)
        self.cache_assoc = int(cache_assoc)
        self.block_size = int(block_size)
        self.repl_policy = repl_policy

        # Se empieza por obtener las constantes utilizadas para describir la caché
        # partiendo de los parámetros dados
        self.byte_offset_size = int(log2(self.block_size))
                                                        # Tamaño, en bits,
                                                        # del byte offset.
        self.num_sets = int((self.cache_capacity *      # Número de sets de caché
                             1024)/(self.block_size * self.cache_assoc))
        self.index_size = int(log2(self.num_sets))      # Tamaño necesario para
                                                        # indexar la caché, en
                                                        # bits
        self.tag_size = int(log2(self.cache_assoc))     # Tamaño en bits del tag

        # Caché se implementa como varias listas
        self.valid_table = [[False for i in range(self.cache_assoc)] for j in range(self.num_sets)]
        self.tag_table = [[0 for i in range(self.cache_assoc)] for j in range(self.num_sets)]
        self.data_age_table = [[0 for i in range(self.cache_assoc)] for j in range(self.num_sets)]

    def print_info(self):
        print("Parámetros del caché:")
        print("\tCapacidad:\t\t\t"+str(self.cache_capacity)+"kB")
        print("\tAssociatividad:\t\t\t"+str(self.cache_assoc))
        print("\tTamaño de Bloque:\t\t\t"+str(self.block_size)+"B")
        print("\tPolítica de Reemplazo:\t\t\t"+str(self.repl_policy))

    def print_stats(self):
        print("Resultados de la simulación")
        miss_rate = (100.0*self.total_misses) / self.total_access
        miss_rate = "{:.3f}".format(miss_rate)
        result_str = str(self.total_misses)+","+miss_rate+"%"
        print(result_str)
        return [self.total_misses, miss_rate]

    def access(self, access_type, address):
        # Antes que nada, se obtiene el índice y la etiqueta que buscar
        # en la caché
        access_byte_offset = int(address%(2**self.byte_offset_size))
        set_index = int((address/(2**self.byte_offset_size))%(2**self.index_size))
        data_tag = int((address/(2**(self.byte_offset_size + self.index_size))))

        # Luego, se busca el dato de en el set de la caché
        data_found = False

        for i in range(self.cache_assoc):
            # Para el índice obtenido, se recorre todas las posibilidades
            # de asociatividad hasta encontrar un dato que sea válido y
            # concuerde con la etiqueta buscada.
            if (self.valid_table[set_index][i] and
                (self.tag_table[set_index][i] == data_tag)):
                data_found = True
                self.data_age_table[set_index][i] = max(self.data_age_table[set_index]) + 1

        # Se  asume que el dato estaba en caché
        access_hit = True

        if data_found == False:
            self.bring_to_cache(set_index, data_tag)
            self.total_misses += 1 
            access_hit = False

        # Se suma 1 a la cantidad total de accesos a la caché
        self.total_access += 1

        return access_hit


    def bring_to_cache(self, set_index, data_tag):
        # Reemplaza el dato a victimizar según la política de reemplazo
        # La primera es la política Least Recently Used
        if self.repl_policy == "l":
            # Obtiene el bloque a victimizar como el que tenga la menor edad de
            # uso
            victim_index =  self.data_age_table[set_index].index(min(self.data_age_table[set_index]))
            # Teniendo el bloque victimizado, se sobreescriben los datos que
            # en él hayan y se coloca su edad de modo que sea el último en
            # victimizarse.
            self.valid_table[set_index][victim_index] = True 
            self.tag_table[set_index][victim_index] = data_tag 
            self.data_age_table[set_index][victim_index] = max(self.data_age_table[set_index]) 
            # Luego, se actualizan las edades de los demás bloques para
            # que no haya dos valores de edad iguales. Esto salvo en los
            # primeros ciclos transitorios, en ellos todas las edades serán
            # de cero.
            for i in range(self.cache_assoc):
                if i != victim_index:
                    self.data_age_table[set_index][i] -= 1
        elif self.repl_policy == "r":
            # En el caso de la política al "r", se escoge el bloque a victimizar
            # al azar
            victim = randint(0, self.cache_assoc - 1)

            self.valid_table[set_index][victim] = True 
            self.tag_table[set_index][victim] = data_tag 

