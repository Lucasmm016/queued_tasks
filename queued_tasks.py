# Script de execução paralela de tarefas com sistema de fila

from asyncio import run, Queue, create_task
from httpx import AsyncClient

base_url = 'https://httpbin.org/get?value={e}'

# função que executa a tarefa utilizando "httpx"
async def my_function(e):
    print("starting task with value", e)
    async with AsyncClient() as c:
        r = await c.get(base_url.format(e=e))
        print("task finished with value", e)
        return r.json() # retorna o resultado da tarefa

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

    # lista de tarefas (parâmetros a ser passado para a requisição)
    list_of_tasks = [
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9
    ]

    results = run(main(NUMBER_OF_TASKS, list_of_tasks, my_function)) # executa a função principal

    print("results:", results) # exibe os resultados gerados
