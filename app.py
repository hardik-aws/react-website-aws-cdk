#!/usr/bin/env python3
import os

import aws_cdk as cdk
from dotenv import load_dotenv

load_dotenv()

from react_website.react_website_stack import ReactWebsiteStack

app = cdk.App()
env= os.environ.get('environment')
application= os.environ.get('application')
# certificateId= os.environ.get('application')

stack_name="%s-%s"%(application,env)

ReactWebsiteStack(app, stack_name,)

app.synth()
