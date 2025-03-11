from collections import deque


class DieHardProblem:
    """Class to represent the 3L and 5L jug problem."""

    def __init__(self):
        self.goal = 4  # The goal is to get exactly 4L in the big jug

    def get_valid_actions(self, small, big):
        """
        Generate all valid next states given the current state (small, big).
        Returns a list of (action_name, (new_small, new_big)).
        """
        actions = []
        if small < 3:  # Fill small jug
            actions.append(("fill_small", (3, big)))
        if big < 5:  # Fill big jug
            actions.append(("fill_big", (small, 5)))
        if small > 0:  # Empty small jug
            actions.append(("empty_small", (0, big)))
        if big > 0:  # Empty big jug
            actions.append(("empty_big", (small, 0)))
        if small > 0 and big < 5:  # Pour small into big
            transfer = min(small, 5 - big)
            actions.append(("pour_small_into_big", (small - transfer, big + transfer)))
        if big > 0 and small < 3:  # Pour big into small
            transfer = min(big, 3 - small)
            actions.append(("pour_big_into_small", (small + transfer, big - transfer)))

        return actions

    def bfs_solve(self):
        """
        Solves the Die Hard water jug problem using Breadth-First Search (BFS).
        This guarantees the shortest sequence of actions to get exactly 4 gallons in the big jug.
        """
        start_state = (0, 0)  # Initial state: both jugs are empty
        queue = deque([(start_state, [])])  # BFS queue (state, action sequence)
        visited = set()  # Track visited states to prevent loops

        while queue:
            # Get the current state and action sequence
            (small, big), actions = queue.popleft()

            # If we reached the goal state (4 gallons in the big jug), return the sequence of actions
            if big == self.goal:
                return actions

            # Skip processing if this state was already visited
            if (small, big) in visited:
                continue
            visited.add((small, big))

            # Generate all valid next states
            for action_name, (new_small, new_big) in self.get_valid_actions(small, big):
                if (new_small, new_big) not in visited:
                    queue.append(((new_small, new_big), actions + [action_name]))

        return None  # No solution found

    def execute_solution(self, solution):
        """
        Execute a given solution step by step and print human-readable output.
        """
        if not solution:
            print("No solution exists.")
            return

        print("\nSolution found!\n")
        print(f"{'Step':<6}{'Action':<20}{'Small Jug (3L)':<15}{'Big Jug (5L)'}")
        print("=" * 50)

        step = 1
        small, big = 0, 0  # Reset to initial state

        for action in solution:
            # Perform the action
            if action == "fill_small":
                small = 3
            elif action == "fill_big":
                big = 5
            elif action == "empty_small":
                small = 0
            elif action == "empty_big":
                big = 0
            elif action == "pour_small_into_big":
                transfer = min(small, 5 - big)
                small -= transfer
                big += transfer
            elif action == "pour_big_into_small":
                transfer = min(big, 3 - small)
                small += transfer
                big -= transfer

            print(f"{step:<6}{action:<20}{small:<15}{big}")
            step += 1


if __name__ == "__main__":
    problem = DieHardProblem()
    solution = problem.bfs_solve()
    problem.execute_solution(solution)


# 📝 Summary of What Happened
# Fill the big jug (5L).
# Pour from big to small until small is full (3L in small, 2L left in big).
# Empty the small jug (0L in small, 2L in big).
# Pour the remaining 2L from big to small (2L in small, 0L in big).
# Fill the big jug again (2L in small, 5L in big).
# Pour from big to small until the small jug is full again (3L in small, ✅ 4L in big).
# 🎉 Correct solution found in 6 moves!
