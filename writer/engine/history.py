import writer.engine.tree as tree
import writer.engine.model as model

class HistoryManager:
    def __init__(self, model_tree: "model.DocumentModelNode"):
        self.__model_tree = model_tree

        # When we make a modification, store the current tree to be able to undo.
        self.__model_tree_before: list[model.DocumentModelNode] = []

        # When we undo, store the current tree to be able to redo.
        self.__model_tree_after: list[model.DocumentModelNode] = []

    def modify(self, position: "tree.Position", **kwargs):
        new_model_tree = tree.new_tree_with_modified_node(position, **kwargs)

        self.__model_tree_after.clear()
        self.__model_tree_before.append(self.__model_tree)
        self.__model_tree = new_model_tree

# Initialized by main.
# FIXME: Find a better way to achieve this.
global_history_manager: HistoryManager = None
