# AWS CDK S3 + Lambda Demo

This is a small event-driven AWS project built with AWS CDK.

## What it does

When a file is uploaded to S3, it automatically triggers a Lambda function.
The Lambda function writes logs to CloudWatch.

## Architecture

User uploads file  
↓  
S3 bucket  
↓  
ObjectCreated event  
↓  
Lambda function  
↓  
CloudWatch logs

## Project structure

small-cdk-s3/
├── infra/
│   ├── lib/
│   │   └── infra-stack.ts
│   ├── bin/
│   ├── cdk.json
│   ├── package.json
│   └── ...
├── lambda/
│   └── index.py
└── README.md

## Files

### infra/lib/infra-stack.ts
Defines:
- S3 bucket
- Lambda function
- S3 event notification
- CloudFormation outputs

### lambda/index.py
Simple Lambda handler that:
- prints a success message
- prints the incoming event
- returns statusCode 200

## Prerequisites

Make sure you have:
- Node.js 20+
- npm
- AWS CLI
- AWS CDK
- Python 3

## Setup

### 1. Configure AWS
```bash
aws configure