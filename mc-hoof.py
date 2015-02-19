#!/home/smoke/pyEnvs/mchoof/bin/python2

import os
from mchoof.management import project


if __name__ == '__main__':
    project.Command(project_path=os.getcwd())
