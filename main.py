import geopandas as gpd
import matplotlib.pyplot as plt

# Definindo as variáveis e seus domínios
variables = ['N', 'CO']
domains = {
    'N': ['vermelho', 'amarelo', 'marrom'],
    'CO': ['azul', 'amarelo', 'marrom']
}

# Definindo as restrições
def constraints(assignment):
    if 'N' in assignment and assignment['N'] != 'vermelho':
        return False
    if 'CO' in assignment and assignment['CO'] != 'azul':
        return False
    return True

# Algoritmo de backtracking
def backtracking(assignment):
    if len(assignment) == len(variables):
        return assignment
    
    unassigned = [v for v in variables if v not in assignment]
    first = unassigned[0]
    
    for value in domains[first]:
        local_assignment = assignment.copy()
        local_assignment[first] = value
        
        if constraints(local_assignment):
            result = backtracking(local_assignment)
            if result is not None:
                return result
    
    return None

# Executando o algoritmo de backtracking
solution = backtracking({})
print(solution)

# Função para mapear as cores
def get_color(region, solution):
    colors = {
        'vermelho': 'red',
        'azul': 'blue',
        'amarelo': 'yellow',
        'marrom': 'brown'
    }
    return colors[solution[region]]

# Carregar dados geoespaciais dos estados do Brasil
brazil_states = gpd.read_file('https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson')

# Definir as regiões e suas subdivisões
regions = {
    'N': ['Acre', 'Amapá', 'Amazonas', 'Pará', 'Rondônia', 'Roraima', 'Tocantins'],
    'CO': ['Distrito Federal', 'Goiás', 'Mato Grosso', 'Mato Grosso do Sul']
}

# Plotar o mapa do Brasil
fig, ax = plt.subplots(1, 1, figsize=(10, 10))

brazil_states.boundary.plot(ax=ax, linewidth=1)

# Colorir as regiões conforme a solução encontrada
for region, states in regions.items():
    for state in states:
        brazil_states[brazil_states.name == state].plot(ax=ax, color=get_color(region, solution))

plt.title('Coloração das Regiões Norte e Centro-Oeste do Brasil')
plt.show()
