import writer.engine.tree as tree
import writer.engine.model as model

class HistoryManager:
    def __init__(self, *, model_tree: "model.DocumentModelNode"):
        self.__model_tree = model_tree

        # When we make a modification, store the current tree to be able to undo.
        self.__model_tree_before: list[model.DocumentModelNode] = []

        # When we undo, store the current tree to be able to redo.
        self.__model_tree_after: list[model.DocumentModelNode] = []

        self.__on_history_change_callbacks = []

    def notify_on_history_change(self, callback):
        self.__on_history_change_callbacks.append(callback)

    def on_history_change(self):
        for callback in self.__on_history_change_callbacks:
            callback()

    def lookup_node(self, *, key_path: list[int]) -> model.ModelNode:
        assert key_path[0] == self.__model_tree.key
        return self.__model_tree.lookup_node_recursively(key_path=key_path[1:])

    def replace_node(self, *, key_path: list[int], new_node: model.ModelNode):
        assert key_path[0] == self.__model_tree.key

        new_model_tree = self.__model_tree.replace_node_recursively(
            key_path=key_path[1:],
            new_node=new_node,
        )

        self.update_model_tree(new_model_tree=new_model_tree)

    def update_model_tree(self, *, new_model_tree: model.DocumentModelNode):
        self.__model_tree_after.clear()
        self.__model_tree_before.append(self.__model_tree)
        self.__model_tree = new_model_tree

        self.on_history_change()

    def get_model_tree(self):
        return self.__model_tree

    def is_undo_possible(self):
        return len(self.__model_tree_before) >= 1

    def is_redo_possible(self):
        return len(self.__model_tree_after) >= 1

    def undo(self):
        assert self.is_undo_possible()

        self.__model_tree_after.append(self.__model_tree)
        self.__model_tree = self.__model_tree_before.pop()

        self.on_history_change()

    def redo(self):
        assert self.is_redo_possible()

        self.__model_tree_before.append(self.__model_tree)
        self.__model_tree = self.__model_tree_after.pop()

        self.on_history_change()

# Initialized by main.
# FIXME: Find a better way to achieve this.
global_history_manager: HistoryManager = None
