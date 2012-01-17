#!/usr/bin/env python
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
os.environ["DJANGO_SETTINGS_MODULE"] = "test_settings"

if __name__ == "__main__":
    from django.core.management import call_command
    call_command("test", "cbv_utils")
