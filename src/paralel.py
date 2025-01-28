from multiprocessing import Pool
import time
import math

N = 5000000

def cube(x):
    return math.sqrt(x)

if __name__ == "__main__":
    
    # first way, using multiprocessing
    start_time = time.perf_counter()
    with Pool() as pool:
      result = pool.map(cube, range(10,N))
    finish_time = time.perf_counter()
    print("Program finished in {} seconds - using multiprocessing".format(finish_time-start_time))
    print("---")

    # second way, serial computation
    start_time = time.perf_counter()
    result = []
    for x in range(10,N):
        result.append(cube(x))
    finish_time = time.perf_counter()

    print("Program finished in {} seconds".format(finish_time-start_time))

# from multiprocessing import Pool
# import os

# # Função que será executada em paralelo
# def trabalho_pesado(numero):
#     pid = os.getpid()  # Obtém o ID do processo
#     print(f"Processo {pid} está processando o número {numero}")
#     return numero ** 2


# if __name__ == "__main__":
#     dados = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
#     # Criação do pool de processos
#     with Pool(processes=os.cpu_count()) as pool:  # 'processes' define o número de processos paralelos
#         resultados = pool.map(trabalho_pesado, dados)  # Distribui os dados nos processos
    
#     print("Resultados:", resultados)
