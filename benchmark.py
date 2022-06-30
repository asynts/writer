import time
import typing
import argparse
import collections

import writer.example
import writer.engine.converter
import writer.engine.model
import writer.engine.layout
import writer.engine.tree as tree

from PyQt6 import QtWidgets

def main(*, b_human_readable: bool):
    measurements = collections.OrderedDict()

    application = QtWidgets.QApplication([])

    writer.engine.layout.dots_per_cm = 37.79527559055118

    model_tree = writer.example.create_model_tree_study(b_print_document_name=False)

    measurement_initial(model_tree=model_tree, measurements=measurements)
    measurement_change_nothing(model_tree=model_tree, measurements=measurements)

    model_tree = modify_first_paragraph(model_tree=model_tree)
    measurement_change_start(model_tree=model_tree, measurements=measurements)

    model_tree = modify_last_paragraph(model_tree=model_tree)
    measurement_change_end(model_tree=model_tree, measurements=measurements)

    if b_human_readable:
        print_measurements_human_readable(measurements)
    else:
        print_measurements_csv(measurements)

def print_measurements_csv(measurements: collections.OrderedDict, /):
    print("measurement_identifier,nanoseconds")

    for identifier, nanoseconds in measurements.items():
        print(f"{identifier},{nanoseconds}")

def print_measurements_human_readable(measurements: collections.OrderedDict, /):
    for identifier, nanoseconds in measurements.items():
        prefix = f"{identifier:}"
        milliseconds = f"{nanoseconds // (1000 * 1000):10}"

        print(f"{prefix:<30}{milliseconds:>10}ms {nanoseconds:12}ns")

# This is a separate function to make the flame graph easier to navigate.
def measurement_initial(*, model_tree, measurements):
    regenerate_layout(model_tree=model_tree, measurements=measurements, identifier="layout_initial")

# This is a separate function to make the flame graph easier to navigate.
def measurement_change_nothing(*, model_tree, measurements):
    regenerate_layout(model_tree=model_tree, measurements=measurements, identifier="layout_change_nothing")

# This is a separate function to make the flame graph easier to navigate.
def measurement_change_start(*, model_tree, measurements):
    regenerate_layout(model_tree=model_tree, measurements=measurements, identifier="layout_change_start")

# This is a separate function to make the flame graph easier to navigate.
def measurement_change_end(*, model_tree, measurements):
    regenerate_layout(model_tree=model_tree, measurements=measurements, identifier="layout_change_end")

def regenerate_layout(
    *,
    model_tree: writer.engine.model.DocumentModelNode,
    measurements: collections.OrderedDict,
    identifier: str,
):
    before_ns = time.perf_counter_ns()
    layout_tree = writer.engine.converter.generate_layout_for_model(model_tree)
    after_ns = time.perf_counter_ns()

    measurements[identifier] = after_ns - before_ns

    return layout_tree

def modify_first_paragraph(*, model_tree: writer.engine.model.DocumentModelNode):
    paragraph_node = model_tree.children[0]
    text_chunk_node = paragraph_node.children[0]

    return tree.new_tree_with_modified_node(
        tree.Position(
            node=text_chunk_node,
            parent_nodes=[
                model_tree,
                paragraph_node,
            ],
        ),
        text="This is a new title!"
    ).root

def modify_last_paragraph(*, model_tree: writer.engine.model.DocumentModelNode):
    paragraph_node = model_tree.children[-1]
    text_chunk_node = paragraph_node.children[-1]

    return tree.new_tree_with_modified_node(
        tree.Position(
            node=text_chunk_node,
            parent_nodes=[
                model_tree,
                paragraph_node,
            ],
        ),
        text=text_chunk_node.text + " THIS HAS BEEN ADDED!",
    ).root

if __name__ == "__main__":
    parser = argparse.ArgumentParser("benchmark")

    parser.add_argument("--human-readable", action="store_true")

    namespace = parser.parse_args()

    main(b_human_readable=namespace.human_readable)
