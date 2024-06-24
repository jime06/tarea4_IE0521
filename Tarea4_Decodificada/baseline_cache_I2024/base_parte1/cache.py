from math import log2, floor
from random import randint

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
        self.byte_offset_size = log2(self.block_size)   # Tamaño del byte offset
        self.num_sets = int((self.cache_capacity *      # Número de sets de caché
                             1024)/(self.block_size * self.cache_assoc))
        self.index_size = int(log2(self.num_sets))      # Tamaño necesario para
                                                        # indexar la caché
#        self.cache_table = {{i: {"tag": 12, "valid": False, "age": 0} for i in range(sef.num_sets)}}
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

    def access(self, access_type, address):
        # Antes que nada, se obtiene el índice y la etiqueta que buscar
        # en la caché
        cache_index = int(floor(address/(2**self.byte_offset_size))%(2**self.index_size))
        cache_tag = int(floor(address/(2**(self.byte_offset_size + self.index_size))))

        # Luego, se busca el dato de en la caché
        found_data = -1
        for i in range(self.cache_assoc):
            # Para el índice obtenido, se recorre todas las posibilidades
            # de asociatividad hasta encontrar un dato que sea válido y
            # concuerde con la etiqueta buscada.
            if (self.valid_table[cache_index][i] and
                (self.tag_table[cache_index][i] == cache_tag)):
                found_data = i

#        access_hit = False # TODO Tal vez esto se use en las cachés multinivel

        if found_data == -1:
            self.bring_to_cache(cache_index, cache_tag)
            self.total_misses += 1 
#            access_hit = True 



        # Se suma 1 a la cantidad total de accesos a la caché
        self.total_access += 1



    def bring_to_cache(self, cache_index, cache_tag):
        # Esta función se encarga de traer un dato a caché

        # Empieza por asumir la ubicación del dato buscado en memoria
        data_location =-1

        # Luego, recorre todas las vías para determinar cuál está disponible
        # para escritura
        for i in range (self.cache_assoc):
            if not(self.valid_table[cache_index][i]):
                self.valid_table[cache_index][i] = True 
                self.tag_table[cache_index][i] = cache_tag 
                self.data_age_table[cache_index][i] = self.cache_assoc - 1 
                data_location = i
                break

        # Luego, reemplaza el dato a victimizar según la política de reemplazo
        # La primera es la política Least Recently Used
        if self.repl_policy == "l":
            # El valor de edad máximo de usos está dado por la asociatividad,
            # se suma uno para asegurar que el límite empiece muy arriba y
            # vaya bajando. Así se escoge cuál bloque victimizar.
            victim =  self.cache_assoc

            # Luego, se recorre todos los datos en la vía para encontrar el
            # que se haya usado menos últimamente
            for i in range(self.cache_assoc):
                temp_victim = self.data_age_table[cache_index][i]
                if temp_victim < victim:
                    victim = i
            # Teniendo el bloque victimizado, se sobreescriben los datos que
            # en él hayan y se coloca su edad de modo que sea el último en
            # victimizarse.
            self.valid_table[cache_index][victim] = True 
            self.tag_table[cache_index][victim] = cache_tag 
            self.data_age_table[cache_index][victim] = self.cache_assoc - 1
            # Luego, se actualizan las edades de los demás bloques para
            # que no haya dos valores de edad iguales. Esto salvo en los
            # primeros ciclos transitorios, en ellos todas las edades serán
            # de cero.
            for i in range(self.cache_assoc):
                if i != victim:
                    self.data_age_table[cache_index][i] -= 1
        elif self.repl_policy == "r":
            # En el caso de la política al "r", se escoge el bloque a victimizar
            # al azar
            victim = randint(0, self.cache_assoc - 1)

            self.valid_table[cache_index][victim] = True 
            self.tag_table[cache_index][victim] = cache_tag 













































