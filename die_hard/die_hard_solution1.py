import json
from langchain_community.chat_models import ChatOllama
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.tools import tool
from hypothesis import note, settings
from hypothesis.stateful import RuleBasedStateMachine, rule, invariant

# Hypothesis settings
settings.register_profile("stateful", max_examples=100)
settings.load_profile("stateful")


class DieHardProblem(RuleBasedStateMachine):
    """Stateful representation of the Die Hard problem with two jugs."""

    small = 0  # 3L Jug (Initially empty)
    big = 0  # 5L Jug (Initially empty)

    @rule()
    def fill_small(self):
        """Fill the small 3L jug completely."""
        self.small = 3

    @rule()
    def fill_big(self):
        """Fill the big 5L jug completely."""
        self.big = 5

    @rule()
    def empty_small(self):
        """Empty the small 3L jug."""
        self.small = 0

    @rule()
    def empty_big(self):
        """Empty the big 5L jug."""
        self.big = 0

    @rule()
    def pour_small_into_big(self):
        """Pour water from the small (3L) jug into the big (5L) jug until full or empty."""
        old_big = self.big
        self.big = min(5, self.big + self.small)
        self.small -= self.big - old_big

    @rule()
    def pour_big_into_small(self):
        """Pour water from the big (5L) jug into the small (3L) jug until full or empty."""
        old_small = self.small
        self.small = min(3, self.small + self.big)
        self.big -= self.small - old_small

    @invariant()
    def physics_of_jugs(self):
        """Ensure the water levels remain within the jugs' capacity constraints."""
        assert 0 <= self.small <= 3
        assert 0 <= self.big <= 5

    @invariant()
    def die_hard_problem_not_solved(self):
        """Ensure the big jug does not contain 4L as part of the problem constraints."""
        note(f"> small: {self.small} big: {self.big}")
        assert self.big != 4


# Tool functions to allow AI to manipulate jugs
@tool
def fill_small():
    """Fill the 3L jug completely."""
    state.fill_small()
    return "Filled small jug to 3L."


@tool
def fill_big():
    """Fill the 5L jug completely."""
    state.fill_big()
    return "Filled big jug to 5L."


@tool
def empty_small():
    """Empty the 3L jug."""
    state.empty_small()
    return "Emptied small jug."


@tool
def empty_big():
    """Empty the 5L jug."""
    state.empty_big()
    return "Emptied big jug."


@tool
def pour_small_into_big():
    """Pour water from the small jug into the big jug until full or empty."""
    state.pour_small_into_big()
    return f"Poured from small to big. Small: {state.small}L, Big: {state.big}L."


@tool
def pour_big_into_small():
    """Pour water from the big jug into the small jug until full or empty."""
    state.pour_big_into_small()
    return f"Poured from big to small. Small: {state.small}L, Big: {state.big}L."


@tool
def get_state():
    """Return the current state of the water levels in both jugs as a JSON object."""
    return json.dumps({"small": state.small, "big": state.big})


# Tool registry
tools = {
    "fill_small": fill_small,
    "fill_big": fill_big,
    "empty_small": empty_small,
    "empty_big": empty_big,
    "pour_small_into_big": pour_small_into_big,
    "pour_big_into_small": pour_big_into_small,
    "get_state": get_state,
}

# Use only Ollama (no OpenAI)
llm = ChatOllama(model="qwen2.5")  # Change model if needed


def solve_die_hard():
    """Main function where AI interacts with the tools to solve the Die Hard problem."""
    print("🧊🥤 Die Hard Water Jug Problem 🧊🥤")
    messages = [
        HumanMessage(
            content="Solve the Die Hard problem using the available tools."
            "Tools are the actions that can be performed on the jugs. If violation occurs, than call get_state tool."
            "Invariants are the constraints that must be maintained:"
            "* Small jug must contain 0 to 3 liters of water,"
            "* Big jug must contain 0 to 5 liters of water,"
            "* Big jug must not contain 4 liters of water. "
            "You must stop when the big jug contains 4 liters of water."
            "Show human readable output for each tool action and the AI's decision."
            "Show exactly how you think in the output during task execution"
        )
    ]
    while True:
        response = llm.invoke(messages)
        ai_action = response.content.strip()

        print(f"AI action: {ai_action}")  # Print AI's decision

        if ai_action == "get_state":
            state_message = get_state()
            messages.append(ToolMessage(content=state_message))
            continue

        if ai_action in tools:
            tool_function = tools[ai_action]
            tool_response = tool_function()
            print(f"Tool output: {tool_response}")  # Print tool result
            messages.append(ToolMessage(content=tool_response))

        state_json = json.loads(get_state())
        if state_json["big"] == 4:
            print("✅ Solution Found: 4L in the big jug!")
            break


# Create an instance of the state machine
state = DieHardProblem()

# Solve the problem
solve_die_hard()
