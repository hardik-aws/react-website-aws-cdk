import aws_cdk as core
import aws_cdk.assertions as assertions

from react_website.react_website_stack import ReactWebsiteStack

# example tests. To run these tests, uncomment this file along with the example
# resource in react_website/react_website_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = ReactWebsiteStack(app, "react-website")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
