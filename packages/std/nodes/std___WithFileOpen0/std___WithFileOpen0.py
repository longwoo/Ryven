from custom_src.NodeInstance import NodeInstance
from custom_src.Node import Node
from custom_src.retain import M


# GENERAL
# self.input(index)                   <- access to input data
# self.outputs[index].set_val(val)    <- set output data port value
# self.main_widget                    <- access to main widget
# self.exec_output(index)             <- executes an execution output

# EDITING
# self.create_new_input(type_, label, widget_name=None, widget_pos='under', pos=-1)
# self.delete_input(input or index)
# self.create_new_output(type_, label, pos=-1)
# self.delete_output(output or index)


# LOGGING
# mylog = self.new_log('Example Log')
# mylog.log('I\'m alive!!')
# self.log_message('hello global!', 'global')
# self.log_message('that\'s not good', 'error')


class WithFileOpen_NodeInstance(NodeInstance):
    def __init__(self, parent_node: Node, flow, configuration=None):
        super(WithFileOpen_NodeInstance, self).__init__(parent_node, flow, configuration)

        # self.special_actions['action name'] = {'method': M(self.action_method)}

        self.initialized()


    def update_event(self, input_called=-1):
        if input_called == 0:
            with open(self.input(1), self.input(2)) as f:
                self.outputs[1].set_val(f)
                self.exec_output(0)

    def get_data(self):
        data = {}
        # ...
        return data

    def set_data(self, data):
        pass


    def remove_event(self):
        pass
