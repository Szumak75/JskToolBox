# -*- coding: utf-8 -*-
"""
  path.py
  Author : Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 15.10.2024, 00:00:38
  
  Purpose: 
"""

import random
import math
import time
from typing import Optional, List, Tuple, Dict


def distance(point_1: List[float], point_2: List[float]) -> Optional[float]:
    """Calculate distance  between two points in 3D space"""
    try:
        return math.dist(point_1, point_2)
    except Exception as ex:
        print(f"{ex}")
    return None


class StarsSystem:

    star_pos: Optional[List[float]] = None
    data: Optional[Dict] = None

    def __init__(self, x: float, y: float, z: float) -> None:
        self.star_pos = [x, y, z]
        self.data = {}

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(star_pos={self.star_pos}, data={self.data})"


class AlgSimulatedAnnealing:
    def __init__(
        self,
        start: StarsSystem,
        systems: List[StarsSystem],
        jump_range: float,
    ) -> None:
        self.start = start
        self.systems = systems
        self.jump_range = jump_range
        self.initial_temp = 1000.0  # 1000
        self.cooling_rate = 0.003  # 0.003
        # initial_temp: Im wyższa temperatura początkowa, tym większe jest
        # prawdopodobieństwo zaakceptowania gorszych rozwiązań na początku procesu.
        # cooling_rate: Kontroluje tempo chłodzenia. Im mniejsza wartość,
        # tym wolniejsze chłodzenie, co pozwala na dokładniejszą eksplorację
        # przestrzeni rozwiązań, ale wydłuża czas działania algorytmu.

        # Aby zoptymalizować działanie algorytmu SA, możesz dostosować:
        # Temperaturę początkową (initial_temp): większe wartości pozwalają
        # na większą eksplorację na początku.
        # Tempo chłodzenia (cooling_rate): wolniejsze tempo daje większe
        # szanse na znalezienie optymalnych rozwiązań, ale wydłuża czas działania.
        # Liczbę iteracji: algorytm może przerywać działanie, gdy temperatura
        # osiągnie bardzo niską wartość.

    def calculate_total_distance(self, path: List[StarsSystem]) -> float:
        """Calculate the total distance of the path, starting from the start point."""
        total_dist = 0
        current_star = self.start
        for next_star in path:
            dist = distance(current_star.star_pos, next_star.star_pos)
            if dist <= self.jump_range:  # Only count valid jumps
                total_dist += dist
            else:
                return float("inf")  # Penalize paths that exceed jump_range
            current_star = next_star
        return total_dist

    def accept_solution(
        self, current_distance: float, new_distance: float, temperature: float
    ) -> bool:
        """Decide whether to accept the new solution based on the current temperature."""
        if new_distance < current_distance:
            return True
        # Accept worse solutions with a probability depending on the temperature
        return random.random() < math.exp(
            (current_distance - new_distance) / temperature
        )

    def run(self) -> List[StarsSystem]:
        """Perform the Simulated Annealing optimization."""
        start_t = time.time()

        # precalculate
        systems: List[StarsSystem] = []
        for item in self.systems:
            if distance(self.start.star_pos, item.star_pos) > 100:
                print(f"{item} removed")
            else:
                systems.append(item)

        self.current_solution = systems[:]
        self.best_solution = systems[:]

        # initial
        random.shuffle(self.current_solution)
        self.best_distance = self.calculate_total_distance(self.current_solution)

        temperature = self.initial_temp
        while temperature > 1:
            # Create a new solution by swapping two random points
            new_solution = self.current_solution[:]
            i, j = random.sample(range(len(new_solution)), 2)
            new_solution[i], new_solution[j] = new_solution[j], new_solution[i]

            # Calculate the total distance for the new solution
            current_distance = self.calculate_total_distance(self.current_solution)
            new_distance = self.calculate_total_distance(new_solution)

            # Decide whether to accept the new solution
            if self.accept_solution(current_distance, new_distance, temperature):
                self.current_solution = new_solution

            # Update the best solution found so far
            if new_distance < self.best_distance:
                self.best_solution = new_solution
                self.best_distance = new_distance

            # Decrease the temperature (cooling)
            temperature *= 1 - self.cooling_rate

        # update distance
        if self.best_solution:
            dist = distance(self.start.star_pos, self.best_solution[0].star_pos)
            self.best_solution[0].data["distance"] = dist
            for item in range(len(self.best_solution) - 1):
                dist = distance(
                    self.best_solution[item].star_pos,
                    self.best_solution[item + 1].star_pos,
                )
                self.best_solution[item + 1].data["distance"] = dist

        end_t = time.time()
        print(f"Evolution took {end_t - start_t} seconds.")
        return self.best_solution

    @property
    def final_distance(self) -> float:
        if not self.best_solution:
            return 0.0
        dist = distance(self.start.star_pos, self.best_solution[0].star_pos)
        for item in range(len(self.best_solution) - 1):
            dist += distance(
                self.best_solution[item].star_pos, self.best_solution[item + 1].star_pos
            )
        return dist if dist else 0.0


class AlgGenetic:

    def __init__(
        self,
        start: StarsSystem,
        systems: List[StarsSystem],
        jump_range: int,
    ) -> None:
        self.start = start
        self.systems = systems
        self.jump_range = jump_range

        self.population: List[List[StarsSystem]] = []
        self.best_solution: List[StarsSystem] = []

        self.population_size = len(systems) * 3  # Rozmiar populacji (100)
        self.generations = 200  # Liczba pokoleń (500)
        self.mutation_rate = 0.01  # Prawdopodobieństwo mutacji (0.01)

        # 1. Rozmiar populacji (population_size):
        # Małe wartości (10-50): Szybsze obliczenia, ale może prowadzić do szybkiej
        # konwergencji do lokalnych optymalnych rozwiązań, zwłaszcza przy bardziej
        # skomplikowanych problemach.
        # Średnie wartości (50-200): Wystarczające dla większości problemów.
        # Dają równowagę pomiędzy różnorodnością rozwiązań a szybkością konwergencji.
        # Duże wartości (200-1000 i więcej): Większa różnorodność, ale znacznie
        # wolniejsze obliczenia. Może być korzystne w bardzo trudnych problemach,
        # gdzie wiele rozwiązań lokalnych wymaga długiego czasu na znalezienie
        # rozwiązania globalnego.

        # Rekomendacja:
        # Zaczynaj od wartości w zakresie 50-100. Dla mniejszych problemów możesz
        # próbować 20-50, a dla większych problemów (np. setki punktów) warto
        # eksperymentować z wartościami 100-500.

        # 2. Liczba generacji (generations):
        # Małe wartości (10-100): Może być wystarczające w przypadku prostych problemów,
        # ale algorytm może nie zdążyć znaleźć optymalnych rozwiązań.
        # Średnie wartości (100-1000): Często wystarczają do osiągnięcia dobrego kompromisu
        # między czasem obliczeń a jakością rozwiązania.
        # Duże wartości (1000-5000 i więcej): Dają algorytmowi więcej czasu na eksplorację
        # i poprawę rozwiązań, ale mogą znacząco wydłużyć czas działania.

        # Rekomendacja:
        # Warto zaczynać od wartości w zakresie 200-500. Jeśli widzisz, że algorytm osiąga
        # zadowalające rozwiązania wcześnie, możesz zmniejszyć liczbę generacji.
        # W przypadku bardziej złożonych problemów, możesz zwiększyć liczbę generacji do 1000-2000.

        # 3. Współczynnik mutacji (mutation_rate):
        # Bardzo małe wartości (0.001-0.01): Utrzymują stabilność populacji, co jest dobre,
        # gdy mamy dobrze zdefiniowane populacje i mało zaburzeń jest potrzebnych. Mogą
        # jednak prowadzić do zbyt wczesnej konwergencji.
        # Średnie wartości (0.01-0.05): Najczęściej stosowane. Dają odpowiednią równowagę
        # między eksploracją nowych rozwiązań a eksploatacją istniejących. Pomaga utrzymać
        # różnorodność populacji bez zbytniego zakłócania dobrych rozwiązań.
        # Duże wartości (0.05-0.3): Wprowadzają dużo różnorodności, co może pomóc
        # w uniknięciu lokalnych minimów, ale może również sprawić, że dobre rozwiązania zostaną przypadkowo zepsute.

        # Rekomendacja:
        # Zacznij od wartości w przedziale 0.01-0.05. Jeśli zauważysz, że algorytm zbyt
        # szybko osiąga stabilizację (lokalne optimum), rozważ zwiększenie współczynnika
        # mutacji. Jeśli natomiast zbyt wiele dobrych rozwiązań jest niszczonych przez
        # mutacje, zmniejsz ten współczynnik.

    def initialize_population(self) -> None:
        """Initialize the population with random routes."""
        for _ in range(self.population_size):
            route = self.systems[:]
            random.shuffle(route)
            self.population.append(route)

    def fitness(self, route: List[StarsSystem]) -> float:
        """Calculate the fitness (inverse of the total route distance)."""
        total_distance = 0.0
        current_point = self.start
        for system in route:
            total_distance += distance(current_point.star_pos, system.star_pos)
            current_point = system
        # Add distance back to the start if needed (optional for closed loop)
        return 1 / total_distance  # Inverse, because shorter routes are better

    def selection(self) -> Tuple[List[StarsSystem], List[StarsSystem]]:
        """Select two parents based on their fitness (roulette wheel selection)."""
        fitness_values = [self.fitness(route) for route in self.population]
        total_fitness = sum(fitness_values)
        probabilities = [f / total_fitness for f in fitness_values]

        # Select two parents based on the fitness-proportional probabilities
        parent1 = random.choices(self.population, weights=probabilities, k=1)[0]
        parent2 = random.choices(self.population, weights=probabilities, k=1)[0]

        return parent1, parent2

    def crossover(
        self, parent1: List[StarsSystem], parent2: List[StarsSystem]
    ) -> List[StarsSystem]:
        """Perform Order Crossover (OX) to generate a child route."""
        start_idx = random.randint(0, len(parent1) - 1)
        end_idx = random.randint(start_idx, len(parent1) - 1)

        child = [None] * len(parent1)
        child[start_idx:end_idx] = parent1[start_idx:end_idx]

        current_pos = end_idx
        for system in parent2:
            if system not in child:
                if current_pos >= len(parent1):
                    current_pos = 0
                child[current_pos] = system
                current_pos += 1

        return child

    def mutate(self, route: List[StarsSystem]) -> None:
        """Perform swap mutation with a given probability."""
        if random.random() < self.mutation_rate:
            idx1 = random.randint(0, len(route) - 1)
            idx2 = random.randint(0, len(route) - 1)
            route[idx1], route[idx2] = route[idx2], route[idx1]

    def evolve(self) -> None:
        """Run the evolutionary algorithm over several generations."""
        self.initialize_population()

        for _ in range(self.generations):
            new_population = []
            for _ in range(self.population_size // 2):  # Generate new population
                parent1, parent2 = self.selection()
                child1 = self.crossover(parent1, parent2)
                child2 = self.crossover(parent2, parent1)
                self.mutate(child1)
                self.mutate(child2)
                new_population.extend([child1, child2])

            # Replace old population with new population
            self.population = new_population

        # Save the best solution found
        self.best_solution = max(self.population, key=self.fitness)

    def run(self) -> List[StarsSystem]:
        """Return the best route found after evolution."""
        start_t = time.time()

        # precalculate
        systems: List[StarsSystem] = []
        for item in self.systems:
            if distance(self.start.star_pos, item.star_pos) > 100:
                print(f"{item} removed")
            else:
                systems.append(item)
        self.systems = systems

        self.evolve()
        # update distance
        if self.best_solution:
            dist = distance(self.start.star_pos, self.best_solution[0].star_pos)
            self.best_solution[0].data["distance"] = dist
            for item in range(len(self.best_solution) - 1):
                dist = distance(
                    self.best_solution[item].star_pos,
                    self.best_solution[item + 1].star_pos,
                )
                self.best_solution[item + 1].data["distance"] = dist

        end_t = time.time()
        print(f"Evolution took {end_t - start_t} seconds.")
        return self.best_solution

    @property
    def final_distance(self) -> float:
        if not self.best_solution:
            return 0.0
        dist = distance(self.start.star_pos, self.best_solution[0].star_pos)
        for item in range(len(self.best_solution) - 1):
            dist += distance(
                self.best_solution[item].star_pos, self.best_solution[item + 1].star_pos
            )
        return dist if dist else 0.0


class AlgGeneric:

    start: Optional[StarsSystem] = None
    systems: Optional[List[StarsSystem]] = None
    jump_range: Optional[int]
    best_solution: List[StarsSystem]

    def __init__(
        self, start: StarsSystem, systems: List[StarsSystem], jump_range: int
    ) -> None:
        self.start = start
        self.systems = systems
        self.jump_range = jump_range
        self.best_solution = []

    def run(self) -> List[StarsSystem]:
        """Algorytm Genetyczny wyszukujący najkrótszą ścieżkę od punktu start,
        poprzez punkty z listy systems przy założeniach:
         - boki grafu o długości przekraczającej jump_range są wykluczone,
         - algorytm ma przejść przez jak największą liczbę punktów,
         - każdy punkt odwiedzany jest tylko raz,
         - wynikowa lista punktów bez punktu startowego umieszczana jest w self.__final
        """

        start_t = time.time()
        current_point = self.start

        # precalculate
        systems: List[StarsSystem] = []
        for item in self.systems:
            if distance(self.start.star_pos, item.star_pos) > 100:
                print(f"{item} removed")
            else:
                systems.append(item)

        remaining_systems = systems  # lista punktów do odwiedzenia

        while remaining_systems:
            # Szukamy najbliższego punktu, który jest w zasięgu jump_range z obecnego punktu
            next_point = None
            min_distance = float("inf")

            for system in remaining_systems:
                dist = distance(current_point.star_pos, system.star_pos)
                if dist is not None and dist <= self.jump_range and dist < min_distance:
                    next_point = system
                    min_distance = dist

            if next_point is None:
                # Nie znaleziono żadnego punktu w zasięgu jump_range
                break

            # Przechodzimy do znalezionego punktu i usuwamy go z listy
            self.best_solution.append(next_point)
            remaining_systems.remove(next_point)
            current_point = next_point  # Aktualizujemy bieżący punkt

        # update distance
        if self.best_solution:
            dist = distance(self.start.star_pos, self.best_solution[0].star_pos)
            self.best_solution[0].data["distance"] = dist
            for item in range(len(self.best_solution) - 1):
                dist = distance(
                    self.best_solution[item].star_pos,
                    self.best_solution[item + 1].star_pos,
                )
                self.best_solution[item + 1].data["distance"] = dist

        end_t = time.time()
        print(f"Evolution took {end_t - start_t} seconds.")
        return self.best_solution

    @property
    def final_distance(self) -> float:
        if not self.best_solution:
            return 0.0
        dist = distance(self.start.star_pos, self.best_solution[0].star_pos)
        for item in range(len(self.best_solution) - 1):
            dist += distance(
                self.best_solution[item].star_pos, self.best_solution[item + 1].star_pos
            )
        return dist if dist else 0.0


if __name__ == "__main__":

    start = StarsSystem(0.0, 0.0, 0.0)
    systems: List[StarsSystem] = [
        StarsSystem(67.50000, -74.90625, -93.68750),
        StarsSystem(134.12500, 15.09375, -63.87500),
        StarsSystem(124.50000, 4.31250, -49.12500),
        StarsSystem(118.93750, -8.53125, -33.46875),
        StarsSystem(105.96875, -20.87500, -22.21875),
        StarsSystem(95.40625, -33.50000, -11.40625),
        StarsSystem(78.34375, -42.96875, -2.21875),
        StarsSystem(66.84375, -60.65625, -3.84375),
        StarsSystem(60.93750, -75.25000, 10.87500),
        StarsSystem(58.28125, -92.09375, 23.71875),
        StarsSystem(60.50000, -74.90625, -93.68750),
        StarsSystem(13.12500, 15.09375, -63.87500),
        StarsSystem(12.50000, 4.31250, -49.12500),
        StarsSystem(11.93750, -8.53125, -33.46875),
        StarsSystem(10.96875, -20.87500, -22.21875),
        StarsSystem(950.40625, -33.50000, -11.40625),
        StarsSystem(780.34375, -42.96875, -2.21875),
        StarsSystem(6.84375, -60.65625, -3.84375),
        StarsSystem(6.93750, -75.25000, 10.87500),
        StarsSystem(5.28125, -92.09375, 23.71875),
    ]
    jump_range: int = 50
    # alg = AlgSimulatedAnnealing(start, systems, jump_range)
    # alg = AlgGeneric(start, systems, jump_range)
    alg = AlgGenetic(start, systems, jump_range)
    path_genetic = alg.run()
    for item in path_genetic:
        print(item)

    print(f"Best solution distance: {alg.final_distance}")


# #[EOF]#######################################################################
