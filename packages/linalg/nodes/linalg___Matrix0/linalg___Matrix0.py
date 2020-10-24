from NIENV import *


# API METHODS

# self.main_widget        <- access to main widget
# self.update_shape()     <- recomputes the whole shape and content positions

# Ports
# self.input(index)                   <- access to input data
# self.set_output_val(index, val)    <- set output data port value
# self.exec_output(index)             <- executes an execution output

# self.create_new_input(type_, label, widget_name=None, widget_pos='under', pos=-1)
# self.delete_input(index)
# self.create_new_output(type_, label, pos=-1)
# self.delete_output(index)


# Logging
# mylog = self.new_log('Example Log')
# mylog.log('I\'m alive!!')
# self.log_message('hello global!', target='global')
# self.log_message('that\'s not good', target='error')

# ------------------------------------------------------------------------------
import numpy as np


class Matrix_NodeInstance(NodeInstance):
    def __init__(self, params):
        super(Matrix_NodeInstance, self).__init__(params)

        self.special_actions['hide preview'] = {'method': M(self.action_hide_mw)}
        self.main_widget_hidden = False
        self.expression_matrix = None
        self.evaluated_matrix = None

    def update_event(self, input_called=-1):
        self.set_output_val(0, self.evaluated_matrix)

    def parse_matrix(self, s):
        lines = s.splitlines()
        # the list(filter(...)) creates an array of strings for every line
        try:
            self.expression_matrix = np.array([[exp for exp in list(filter(lambda s: s != '', l.split(' ')))] for l in lines])
            self.evaluated_matrix = self.eval_matrix(self.expression_matrix)
            if self.evaluated_matrix is None: return  # matrix could not be parsed
            # custom_array = [list(map(number_type, list(filter(lambda s: s != '', l.split(' '))))) for l in lines]
        except ValueError:
            # something like 2+ (which could become 2+1j) can't get parsed yet
            return
        try:
            self.evaluated_matrix = np.array(self.evaluated_matrix)
        except Exception:
            return
        self.update()

    def eval_matrix(self, lines):
        try:
            v = self.get_var_val
            evaled_exp_array = []
            for l in lines:
                evaled_exp_array.append([])
                for exp in l:
                    # print(exp)
                    # print(eval(exp))
                    evaled_exp_array[-1].append(eval(exp))
            # exp_array = [[eval(exp) for exp in l] for l in lines]
            # already convert pure ints to floats
            float_exp_array = [[float(exp) if type(exp) == int else exp for exp in l] for l in evaled_exp_array]
            return float_exp_array
        except Exception as e:
            print(e)
            return None

    def get_var_val(self, name):
        return self.flow.parent_script.variables_handler.get_var(name).val

    def action_hide_mw(self):
        self.main_widget.hide()
        del self.special_actions['hide preview']
        self.special_actions['show preview'] = {'method': M(self.action_show_mw)}
        self.main_widget_hidden = True
        self.update_shape()

    def action_show_mw(self):
        self.main_widget.show()
        del self.special_actions['show preview']
        self.special_actions['hide preview'] = {'method': M(self.action_hide_mw)}
        self.main_widget_hidden = False
        self.update_shape()

    def get_data(self):
        data = {'main widget hidden': self.main_widget_hidden}
        return data

    def set_data(self, data):
        self.main_widget_hidden = data['main widget hidden']
        if self.main_widget_hidden:
            self.action_hide_mw()
        # shown by default

    def removing(self):
        pass
