"""
This type stub file was generated by pyright.
"""

import logging

LOG = logging.getLogger("bcdocs")

class ReSTDocument(object):
    def __init__(self, target=...) -> None: ...
    def write(self, content):
        """
        Write content into the document.
        """
        ...

    def writeln(self, content):
        """
        Write content on a newline.
        """
        ...

    def peek_write(self):
        """
        Returns the last content written to the document without
        removing it from the stack.
        """
        ...

    def pop_write(self):
        """
        Removes and returns the last content written to the stack.
        """
        ...

    def push_write(self, s):
        """
        Places new content on the stack.
        """
        ...

    def getvalue(self):
        """
        Returns the current content of the document as a string.
        """
        ...

    def translate_words(self, words): ...
    def handle_data(self, data): ...
    def include_doc_string(self, doc_string): ...
    def remove_last_doc_string(self): ...

class DocumentStructure(ReSTDocument):
    def __init__(self, name, section_names=..., target=..., context=...) -> None:
        """Provides a Hierarichial structure to a ReSTDocument

        You can write to it similiar to as you can to a ReSTDocument but
        has an innate structure for more orginaztion and abstraction.

        :param name: The name of the document
        :param section_names: A list of sections to be included
            in the document.
        :param target: The target documentation of the Document structure
        :param context: A dictionary of data to store with the strucuture. These
            are only stored per section not the entire structure.
        """
        ...

    @property
    def name(self):
        """The name of the document structure"""
        ...

    @property
    def path(self):
        """
        A list of where to find a particular document structure in the
        overlying document structure.
        """
        ...

    @path.setter
    def path(self, value): ...
    @property
    def available_sections(self): ...
    @property
    def context(self): ...
    def add_new_section(self, name, context=...):
        """Adds a new section to the current document structure

        This document structure will be considered a section to the
        current document structure but will in itself be an entirely
        new document structure that can be written to and have sections
        as well

        :param name: The name of the section.
        :param context: A dictionary of data to store with the strucuture. These
            are only stored per section not the entire structure.
        :rtype: DocumentStructure
        :returns: A new document structure to add to but lives as a section
            to the document structure it was instantiated from.
        """
        ...

    def get_section(self, name):
        """Retrieve a section"""
        ...

    def delete_section(self, name):
        """Delete a section"""
        ...

    def flush_structure(self):
        """Flushes a doc structure to a ReSTructed string

        The document is flushed out in a DFS style where sections and their
        subsections' values are added to the string as they are visited.
        """
        ...

    def getvalue(self): ...
    def remove_all_sections(self): ...
    def clear_text(self): ...
