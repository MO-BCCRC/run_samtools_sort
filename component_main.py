'''

Created on May 12, 2014

@author: dgrewal
@last updated: 4 Mar 2015 by jrosner
component for running samtools sort
'''

from kronos.utils import ComponentAbstract


class Component(ComponentAbstract):

    def __init__(self,component_name='run_samtools_sort', component_parent_dir=None, seed_dir=None):
        self.version = '1.0.0'
        ## initialize ComponentAbstract
        super(Component, self).__init__(component_name, component_parent_dir, seed_dir)

    def focus(self, cmd, cmd_args, chunk):
        pass

    def make_cmd(self,chunk):
        cmd = self.requirements['samtools']

        self.args.output = self.args.output.replace('.bam','')

        if hasattr(self.args, 'options') and  self.args.options:
            cmd_args = ['sort', 
                        self.args.options,
                        self.args.input, 
                        self.args.output
                        ]
        else:
            cmd_args = ['sort',
                        self.args.input,
                        self.args.output
                        ]
        return cmd, cmd_args

    def test(self):
        import component_test
        component_test.run()

def _main():
    comp = Component()
    comp.args = component_ui.args
    comp.run()
    comp.test()


if __name__ == '__main__':
    import component_ui
    _main()
