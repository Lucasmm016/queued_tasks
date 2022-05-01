# Script
Gerenciador de tarefas agendadas por sistema de fila.
Processo parecido com a função "Parallel" da lib "joblib".

# Exemplo de uso
Possuo uma lista contendo 100 requisições em api's, e é necessário executar de 3 em 3 requisições de forma concorrente (simultaneamente), podendo ser utilizado a lib "httpx".
Neste exemplo o script irá executar 3 tarefas simultâneas, e assim que uma tarefa finalizar, ele já dá início a próxima tarefa que está em uma espécie de "fila", assim mantendo sempre 3 tarefas simultâneas até que a minha lista de requisições termine.

# Referências
Para obter o resultado, foi consultado os seguintes links:
<ol>
  <li>https://stackoverflow.com/questions/48483348/how-to-limit-concurrency-with-python-asyncio</li>
  <li>https://www.pythonfixing.com/2022/01/fixed-how-to-asynciogather-tasks-in.html</li>
</ol>
