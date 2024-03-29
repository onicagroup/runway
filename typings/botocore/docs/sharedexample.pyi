"""
This type stub file was generated by pyright.
"""

class SharedExampleDocumenter(object):
    def document_shared_example(self, example, prefix, section, operation_model):
        """Documents a single shared example based on its definition.

        :param example: The model of the example

        :param prefix: The prefix to use in the method example.

        :param section: The section to write to.

        :param operation_model: The model of the operation used in the example
        """
        ...

    def document_input(self, section, example, prefix, shape): ...
    def document_output(self, section, example, shape): ...

def document_shared_examples(section, operation_model, example_prefix, shared_examples):
    """Documents the shared examples

    :param section: The section to write to.

    :param operation_model: The model of the operation.

    :param example_prefix: The prefix to use in the method example.

    :param shared_examples: The shared JSON examples from the model.
    """
    ...
