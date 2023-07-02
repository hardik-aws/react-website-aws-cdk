
import os
from constructs import Construct
import json
import jsii
from aws_cdk import (
    Duration,
    Stack,
    aws_s3 as s3, 
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as cloudfront_origins,
    CfnOutput,
    aws_certificatemanager as acm,
    Fn
)


acm_id = os.environ.get('certificate_id')
domains = os.getenv("domains")

class ReactWebsiteStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        s3_origin = s3.Bucket(self, 'react_website_bucket',
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            encryption=s3.BucketEncryption.S3_MANAGED
        )

        # S3 Bucket output value
        CfnOutput(self, 'bucketname',
            value= s3_origin.bucket_name,
            description= "Name of S3 bucket to hold website content",
            # export_name= "s3::bucketname",
        )

        #S3 Bucket access permission to only allow from cloudfront access identity
        oia = cloudfront.OriginAccessIdentity(self, 'react_website_oia', comment= domains)
        s3_origin.grant_read(oia)

        #existing ssl certificate
        cert = acm.Certificate.from_certificate_arn( self, "sslCertificate", 
            acm_id)

        ## Cloudfront destribution
        distribution = cloudfront.Distribution(self, "react_website_desctribution",
            certificate=cert,
            minimum_protocol_version=cloudfront.SecurityPolicyProtocol.TLS_V1_2_2018,
            default_root_object="index.html",
            price_class=cloudfront.PriceClass.PRICE_CLASS_ALL,
            default_behavior=cloudfront.BehaviorOptions(
                    allowed_methods=cloudfront.AllowedMethods.ALLOW_ALL,
                    origin=cloudfront_origins.S3Origin(
                        bucket=s3_origin,
                        origin_access_identity=oia,
                        origin_path="/",
                    ),
                    viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
                ),
            domain_names=[domains],    
            error_responses=[
                cloudfront.ErrorResponse(
                        http_status=403,
                        response_page_path="/index.html",
                        response_http_status=200,
                    ),
                cloudfront.ErrorResponse(
                        http_status=404,
                        response_page_path="/index.html",
                        response_http_status=200,
                    )
            ]
        )

        CfnOutput(self, 'Cloudfront',
            value= Fn.get_att(distribution, 'domain_name').to_string(),
            description= "ID of Cloudfront Distribution",
            # export_name= "cloudfront::domain_name",
        )
