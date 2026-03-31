import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as s3n from 'aws-cdk-lib/aws-s3-notifications';

export class InfraStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // Create S3 bucket
    const bucket = new s3.Bucket(this, 'MyFirstBucket', {
      versioned: true,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      autoDeleteObjects: true,
    });

    // Create Lambda function
    const myFunction = new lambda.Function(this, 'MyS3TriggerFunction', {
      runtime: lambda.Runtime.PYTHON_3_11,
      handler: 'index.lambda_handler',
      code: lambda.Code.fromAsset('../lambda'),
    });

    // Configure S3 to trigger Lambda when a new object is created
    bucket.addEventNotification(
      s3.EventType.OBJECT_CREATED,
      new s3n.LambdaDestination(myFunction)
    );

    // Output bucket name
    new cdk.CfnOutput(this, 'BucketName', {
      value: bucket.bucketName,
    });

    // Output Lambda name
    new cdk.CfnOutput(this, 'LambdaName', {
      value: myFunction.functionName,
    });
  }
}