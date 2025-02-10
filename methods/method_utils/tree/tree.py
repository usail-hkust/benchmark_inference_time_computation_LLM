class Node(object):
    def __init__(
        self, parent=None, prior_p=1.0, initial_value=0.0
    ) -> None:
        self._parent = parent
        self._children = {}
        self._visit_count = 0
        self._value_sum = 0
        self.prior_p = prior_p
        self.prior_p_ori = prior_p

        self._initial_value = initial_value
        self._terminated = False

    def __lt__(self, other):
        return self._initial_value < other._initial_value

    @property
    def terminated(self):
        return self._terminated

    def set_as_terminate_node(self):
        self._terminated = True

    @property
    def value(self) -> float:
        if self._visit_count == 0:
            return self._initial_value
        return self._value_sum / self._visit_count

    def update(self, value: float) -> None:
        self._visit_count += 1
        self._value_sum += value

    def is_leaf(self) -> bool:
        return self._children == {}

    def is_root(self) -> bool:
        return self._parent is None

    @property
    def parent(self):
        return self._parent

    @property
    def children(self):
        return self._children

    @property
    def visit_count(self):
        return self._visit_count

    def clear(self):
        self._visit_count = 0
        self._value_sum = 0
        self.prior_p = self.prior_p_ori

class LanguageNode(Node):
    def __init__(
        self,
        parent=None,
        prior_p=1.0,
        prm_value=None,
        text_state=None,
        last_action=None,
        initial_value=0.0,
        num_generated_token=None,
    ) -> None:
        super().__init__(parent, prior_p, initial_value)
        self.text_state = text_state
        self.last_action = last_action
        self.prm_value = prm_value
        self.num_generated_token = num_generated_token
        self.has_collected_token_num = False
        self.depth = parent.depth + 1 if parent else 0

    def get_path(self):
        actions = []
        node = self
        while not node.is_root():
            actions.append(node.last_action)
            node = node.parent
        actions.reverse()
        return " ".join(actions)

    def best_child(self, c_param=1.4):
        choices_weights = [
            (child.value / child.visit_count) + c_param * np.sqrt((2 * np.log(self.visit_count) / child.visit_count))
            for child in self.children.values()
        ]
        return list(self.children.values())[np.argmax(choices_weights)]