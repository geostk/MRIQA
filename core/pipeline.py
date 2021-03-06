"""
pipeline.py
"""
from os import walk
from re import search
from importlib import import_module
from multiprocessing import Process
from pydoc import locate
from lxml import etree

class Pipeline(object):
    """
    pipeline class
    """
    def __init__(self, log_server, file_name):
        super(Pipeline, self).__init__()
        self.log_server = log_server
        self.file_name = file_name

    def run(self):
        """
        startup method
        """
        # read xml file
        pipeline = etree.parse(self.file_name, \
            etree.XMLParser \
            (schema=etree.XMLSchema(etree.XML(open('core/pipeline.xsd', 'r').read()))))
        components = []

        # dynamically load components
        for component in pipeline.xpath('component'):
            # get component class
            for root, _, files in walk('components'):
                for file in files:
                    if search('.py$', file) and component.xpath('name')[0].text in file:
                        class_path = root.replace('/', '.').replace('\\', '.') \
                            + '.' + file.replace('.py', '')

            component_class = getattr(import_module(class_path), component.xpath('class')[0].text)
            # instantiate class
            components.append(component_class(self.read_options(component)))

        # glue components together which aren't disabled with autoglue
        for index, component in enumerate(components):
            if index + 1 < len(components) and components[index + 1].auto_glue:
                component.output_notifier.add_observer(components[index + 1].input_observer)

        # add additional components to component
        for component in components:
            if component.additional_components:
                for additional_component in component.additional_components:
                    for b_comp in components:
                        if b_comp.component_id == additional_component['additional_component_id']:
                            notifier = getattr(b_comp, additional_component['notifier'])
                            notifier.add_observer(component.input_observer)

        # start at component
        process = Process(target=components[0].start)
        process.start()

    def read_options(self, component):
        """
        read options from xml
        """
        options = dict()
        options['log_server'] = self.log_server

        # read id value
        component_id = component.xpath('id')
        if component_id:
            options['component_id'] = component.xpath('id')[0].text
        else:
            options['component_id'] = None

        # read autoglue value
        options['auto_glue'] = component.xpath('autoglue')
        if options['auto_glue']:
            options['auto_glue'] = component.xpath('autoglue')[0].text
            if options['auto_glue'] == 'true':
                options['auto_glue'] = True
            elif options['auto_glue'] == 'false':
                options['auto_glue'] = False
        else:
            options['auto_glue'] = True

        # read properties
        options['properties'] = dict()
        for component_property in component.xpath('property'):
            property_value = component_property.xpath('value')[0]
            property_value_type = component_property.xpath('value/@type')
            # typecast components
            if property_value_type:
                property_type = locate(property_value_type[0])
                property_value = property_type(property_value.text)
            else:
                property_value = property_value.text
            options['properties'][component_property.xpath('name')[0].text] = property_value

        # read additional_component
        options['additional_components'] = []
        for additional_component in component.xpath('additional_component'):
            component_id = additional_component.xpath('id')[0].text
            # by convention notifiers has to end with _notifier
            if additional_component.xpath('notifier'):
                notifier = additional_component.xpath('notifier')[0].text + "_notifier"
            else:
                notifier = "output" + "_notifier"
            options['additional_components'].append(dict(additional_component_id=component_id, \
                                                         notifier=notifier))

        return options
