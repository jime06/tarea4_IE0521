from math import log2 ,floor 
class cache:
    def __init__(self,cache_capacity,cache_assoc,block_size,repl_policy):
        self.total_access = 0 
        self.total_misses = 0 
        self.total_reads = 0 
        self.total_read_misses = 0 
        self.total_writes = 0 
        self.total_write_misses = 0 
        self.cache_capacity = int(cache_capacity)
        self.cache_assoc = int(cache_assoc)
        self.block_size = int(block_size)
        self.repl_policy = repl_policy
        self.byte_offset_size = log2(self.block_size)
        self.num_sets = int((self.cache_capacity * 1024)/(self.block_size * self.cache_assoc))
        self.index_size = int(log2 (self.num_sets))
        self.valid_table = [[False for i in range(self.cache_assoc)] for j in range(self.num_sets)]
        self.tag_table = [[0 for i in range(self.cache_assoc)] for j in range(self.num_sets)]
        self.repl_table = [[0 for i in range(self.cache_assoc)] for j in range(self.num_sets)]

    def print_info(self):
        print ("Parámetros del caché:")
        print ("\tCapacidad:\t\t\t" + str(self.cache_capacity)+" kB")
        print ("\tAssociatividad:\t\t\t" + str(self.cache_assoc))
        print ("\tTamaño de Bloque:\t\t\t" + str(self.block_size)+" B")
        print ("\tPolítica de Reemplazo:\t\t\t" + str(self.repl_policy))

    def print_stats (self):
        print ("Resultados de la simulación")
        percent_tot_misses = (100.0 * self.total_misses)/self.total_access
        percent_tot_misses = "{:.3f}".format(percent_tot_misses)
        percent_read_misses = (100.0 * self.total_read_misses)/self.total_reads 
        percent_read_misses = "{:.3f}".format(percent_read_misses)
        percent_write_missses = (100.0 * self.total_write_misses)/self.total_writes 
        percent_write_missses = "{:.3f}".format(percent_write_missses)
        message = str(self.total_misses) + "," + percent_tot_misses + "%," + str(self.total_read_misses) + ","
        message += percent_read_misses + "%," + str(self.total_write_misses) + "," + percent_write_missses + "%"
        print(message)

    def access(self, access_type, access_address):
        access_byte_offset = int(access_address%(2**self.byte_offset_size))
        cache_index = int(floor(access_address/(2**self.byte_offset_size))%(2**self.index_size))
        cache_tag = int(floor(access_address/(2**(self.byte_offset_size + self.index_size))))
        access_result = self.find(cache_index, cache_tag)
        access_hit = False 
        if access_result == -1:
            self.bring_to_cache(cache_index, cache_tag)
            self.total_misses += 1 
            if access_type == "r":
                self.total_read_misses += 1
            else:
                self.total_write_misses += 1
            access_hit = True 
        self.total_access += 1
        if access_type == "r":
            self.total_reads += 1
        else :
            self.total_writes += 1
        return access_hit 

    def find (self,cache_index, cache_tag):
        for i in range(self.cache_assoc):
            if self.valid_table[cache_index][i] and (self.tag_table[cache_index][i] == cache_tag):
                return i 
        return -1

    def bring_to_cache (self,cache_index ,cache_tag):
        data_location =-1 
        for i in range (self.cache_assoc):
            if not(self.valid_table[cache_index][i]):
                self.valid_table[cache_index][i] = True 
                self.tag_table[cache_index][i] = cache_tag 
                self.repl_table[cache_index][i] = self.cache_assoc - 1 
                data_location = i
                break 
        if self.repl_policy =="l":
            data_age = 999999 
            for i in range(self.cache_assoc):
                data_age_tmp = self.repl_table [cache_index ][i]
                if data_age_tmp < data_age:
                    data_age = i
            self.valid_table[cache_index][data_age] = True 
            self.tag_table[cache_index][data_age] = cache_tag 
            self.repl_table[cache_index][data_age] = self.cache_assoc - 1
            data_location = data_age
            for i in range(self.cache_assoc):
                if i == data_location:
                    continue 
                else:
                    self.repl_table[cache_index][i] -= 1 
