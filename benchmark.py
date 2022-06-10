import time
import typing
import argparse
import collections

import writer.example
import writer.engine.converter
import writer.engine.model
import writer.engine.layout

from PyQt6 import QtWidgets

def main(*, b_human_readable: bool):
    measurements = collections.OrderedDict()

    application = QtWidgets.QApplication([])

    writer.engine.layout.dots_per_cm = 37.79527559055118

    model_tree = writer.example.create_model_tree(b_print_document_name=False)

    measurement_initial(model_tree=model_tree, measurements=measurements) # initial_layout
    regenerate_layout(model_tree=model_tree, measurements=measurements, identifier="layout_unchanged_1")

    modify_first_paragraph(model_tree=model_tree)

    measurement_regenerate_worst(model_tree=model_tree, measurements=measurements) # layout_change_start
    regenerate_layout(model_tree=model_tree, measurements=measurements, identifier="layout_unchanged_2")

    modify_last_paragraph(model_tree=model_tree)

    measurement_regenerate_best(model_tree=model_tree, measurements=measurements) # layout_change_end
    regenerate_layout(model_tree=model_tree, measurements=measurements, identifier="layout_unchanged_3")

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
        seconds = f"{nanoseconds / (1000 * 1000 * 1000):10.4f}"

        print(f"{prefix:<30}{seconds:>10}s {nanoseconds:12}ns")

# This is a separate function to make the flame graph easier to navigate.
def measurement_initial(*, model_tree, measurements):
    regenerate_layout(model_tree=model_tree, measurements=measurements, identifier="initial_layout")

# This is a separate function to make the flame graph easier to navigate.
def measurement_regenerate_worst(*, model_tree, measurements):
    regenerate_layout(model_tree=model_tree, measurements=measurements, identifier="layout_change_start")

# This is a separate function to make the flame graph easier to navigate.
def measurement_regenerate_best(*, model_tree, measurements):
    regenerate_layout(model_tree=model_tree, measurements=measurements, identifier="layout_change_end")

def regenerate_layout(*, model_tree: writer.engine.model.DocumentModelNode, measurements: collections.OrderedDict, identifier: str):
    before_ns = time.perf_counter_ns()
    layout_tree = writer.engine.converter.generate_layout_for_model(model_tree)
    after_ns = time.perf_counter_ns()

    measurements[identifier] = after_ns - before_ns

    return layout_tree

def modify_first_paragraph(*, model_tree: writer.engine.model.DocumentModelNode):
    # We delete the last 'TextChunkModelNode' from the first paragraph.
    first_paragraph: writer.engine.model.ParagraphModelNode = model_tree.get_children()[0]
    del first_paragraph.get_children()[-1]

def modify_last_paragraph(*, model_tree: writer.engine.model.DocumentModelNode):
    # Append some text to the last paragraph.
    last_paragraph: writer.engine.model.ParagraphModelNode = model_tree.get_children()[-1]
    last_text_chunk: writer.engine.model.TextChunkModelNode = last_paragraph.get_children()[-1]
    last_text_chunk.set_text(last_text_chunk.get_text() + " THIS HAS BEEN ADDED!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser("benchmark")

    parser.add_argument("--human-readable", action="store_true")

    namespace = parser.parse_args()

    main(b_human_readable=namespace.human_readable)
