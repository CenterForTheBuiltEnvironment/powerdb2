#!/usr/bin/env python
import os, sys 

PROJECT_ROOT = os.path.dirname(__file__)
sys.path = [os.path.join(PROJECT_ROOT, 'lib'), PROJECT_ROOT] + sys.path
if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
