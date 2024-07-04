#!/usr/bin/python3
# Se encarga de llevar a cabo las simulaciones

'''
Este script ejecuta y salva las pruebas que se deben realizar con el $ 
realizado en la tarea 4
'''

#se importa el archivo a utilizar
import cache
import cache_sim

#Ahora, con la función eval se evalúan los parámetros requeridos para cada cosa
cache_capacity_8 = "cache.__init__(8,8,64,LRU)"
cache_capacity_16 = "cache.__init__(16,8,64,LRU)" 
cache_capacity_32 = "cache.__init__(32,8,64,LRU)"
cache_capacity_64 = "cache.__init__(64,8,64,LRU)"
cache_capacity_128 = "cache.__init__(128,8,64,LRU)"

cache_assoc1 = "cache.__init__(32,1,64,LRU)"
cache_assoc2 = "cache.__init__(32,2,64,LRU)"
cache_assoc4 = "cache.__init__(32,4,64,LRU)"
cache_assoc8 = "cache.__init__(32,8,64,LRU)"
cache_assoc16 = "cache.__init__(32,16,64,LRU)"

block_size16 = "cache.__init__(32,8,16,LRU)"
block_size32 = "cache.__init__(32,8,32,LRU)"
block_size64 = "cache.__init__(32,8,64,LRU)"
block_size128 = "cache.__init__(32,8,128,LRU)"

repl_policyLRU = "cache.__init__(32,8,64,LRU)" #este es como el default
repl_policyrandom = "cache.__init__(32,8,64,random)"

#esto se tiene que impirmir en un archivo