# Script de execução paralela de tarefas com sistema de fila

from asyncio import run, Queue, create_task, sleep
from random import randint

# função exemplo de tarefa (aqui ficaria o request usando httpx por exemplo)
async def my_function(e):
    rand = randint(1, 5) # tempo aleatório para a tarefa ser executada (poderia ser uma requisição)
    print("start task", e, "and sleep for", rand, "seconds")
    await sleep(rand)
    print("end task", e)
    return e # retorna o resultado da tarefa

# função "trabalhadora", onde é catalogado os resultados das tarefas e informa ao "queue" que a tarefa terminou
async def worker(q, r, f: callable):
    while True:
        e = await q.get() # aguarda uma tarefa
        r.append(await f(e)) # adiciona o resultado da tarefa na lista de resultados
        q.task_done() # informa ao gerenciados de tarefas, que uma tarefa terminou

# função principal que designa as tarefas a serem executadas
async def main(n:int, tasks: list, f: callable):
    # n: número de tarefas
    # tasks: lista de tarefas
    # f: função que executa a tarefa

    q = Queue(n) # define o número máximo de tarefas a serem executadas
    r = []

    workers = [create_task(worker(q, r, f)) for _ in range(n)] # informa à função "trabalhora" os parâmetros para a execução das tarefas

    for i in tasks:
        await q.put(i) # envia as tarefas para a fila
    
    await q.join() # aguarda todas as tarefas terminarem

    for w in workers:
        w.cancel() # cancela as tarefas

    return r

if __name__ == "__main__":
    NUMBER_OF_TASKS = 3 # número de tarefas a serem executadas simultaneamente

    # lista de tarefas (apenas um exemplo, mas poderia ser qualquer coisa)
    list_of_tasks = [
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9
    ]

    results = run(main(NUMBER_OF_TASKS, list_of_tasks, my_function)) # executa a função principal

    print("results:", results) # exibe os resultados gerados