'''
Created on Jun 17, 2014

@author: dgrewal
##tests for the count_component
'''

import unittest
import component_reqs, component_main
from collections import defaultdict

class args():
    def __init__(self):
        self.input = '/sample/path/checks/make_cmd/input.bam'
        self.output = '/sample/path/checks/make_cmd/output.bam'
        self.metrics_file = '/sample/path/checks/make_cmd/metrics'
        self.assume_sorted = True
        self.read_name_regex = '[a-zA-Z0-9]+_[0-9]+:[0-9]+:([0-9]+):([0-9]+):([0-9]+).*'
        self.opd = 16,
        self.mfhfrem = 1000,
        self.val_stringency = 'LENIENT'
        self.tmp_dir = '/sample/path/checks/make_cmd/tmp_dir'

class check_requirements(unittest.TestCase):
    def setUp(self):
        self.args = args()
        
    #make sure that the required fields are present in reqs file
    def test_verify_reqs(self):
        try:
            _ = component_reqs.env_vars
            _ = component_reqs.parallel
            _ = component_reqs.requirements
            _ = component_reqs.parallel_param
            _ = component_reqs.version
        except:
            self.assertEqual(True, False, 'Please complete the requirements file')    
    
    def test_make_cmd(self):
        comp = component_main.Component()
        comp.args = self.args
        cmd,cmd_args = comp.make_cmd(chunk=None)
        cmd_args = ' '.join(map(str,cmd_args))
        
        #The actual resulting command:
        real_command =  component_reqs.requirements['java'] +' -Xmx4G -jar ' +\
                        component_reqs.requirements['MarkDuplicates']
                        
        real_command_args = ['INPUT=/sample/path/checks/make_cmd/input.bam',
                             'OUTPUT=/sample/path/checks/make_cmd/output.bam',
                             'METRICS=/sample/path/checks/make_cmd/metrics',
                             'ASSUME_SORTED=TRUE',
                             'READ_NAME_REGEX="[a-zA-Z0-9]+_[0-9]+:[0-9]+:([0-9]+):([0-9]+):([0-9]+).*"',
                             'OPTICAL_DUPLICATE_PIXEL_DISTANCE=16',
                             'MAX_FILE_HANDLES_FOR_READ_ENDS_MAP=1000',
                             'VALIDATION_STRINGENCY=LENIENCY',
                             'TMP_DIR=/sample/path/checks/make_cmd/tmp_dir']
        
        #Ensure that the commands match exactly
        self.assertEqual(real_command, cmd, 'Please recheck the cmd variable in make_cmd')
        
        #Ensure that each of the args are present in the command args list
        #Exact match not possible since order can change 
        for val in real_command_args:
            if not val in cmd_args:
                self.assertEqual(True, False, 'Please recheck the cmd_args list in make_cmd')
                
    def test_params(self):
        try:
            from component_params import input_files,input_params,output_files,return_value
        except:
            self.assertEqual(True,False,'Please complete the params file')
        try:
            import component_ui   
        except:
            #cannot run this test if running in unittest mode as ui isn't available
            self.assertEqual(True, True, '') 
            return
            
        arg_act = defaultdict(tuple)
        for val in component_ui.parser._actions[1:]:
            arg_act[val.dest] = (val.required,val.default)
            if val.required == None:
                self.assertEqual(val.default, None, 'The optional argument: '+ val.dest+' has no default value')
        
        #merge all the dictionaries together
        params_dict = dict(input_files.items() + input_params.items() + output_files.items())
        
        for dest,(req,default) in arg_act.iteritems():
            if req == True:
                self.assertEqual(params_dict[dest], '__REQUIRED__', 'params and ui dont match')
            else:
                if not params_dict[dest] in [default,None]:
                    self.assertEqual(True, False, 'Please ensure that either default or ' +\
                                     '__OPTIONAL__ flag is provided for: '+params_dict[dest])

def run():
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    
    checkreqs = loader.loadTestsFromTestCase(check_requirements)
    
    suite.addTests(checkreqs)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
