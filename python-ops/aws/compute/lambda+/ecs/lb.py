#!/usr/bin/env python3

#python lb.py vpc_id vpc-0c5d756112c4f5cf3  subnet1 subnet-0a6bfbe2292811d1d  subnet2 subnet-0030d7d3cfeab6886  sg sg-01b1b66c3aa25cfde 



import argparse

import boto3


def main():
    parser = argparse.ArgumentParser(description='Deployment of load balancer')
    parser.add_argument('--vpc-id', dest='vpc_id', required=True)
    parser.add_argument('--subnet-1', dest='subnet1', help='Public subnet for AWS Load Balancer', required=True)
    parser.add_argument('--subnet-2', dest='subnet2', help='Public subnet for AWS Load Balancer', required=True)
    parser.add_argument('--security-group', dest='sg', help='Security group for AWS Load Balancer.', required=True)
    args = parser.parse_args()

    elbv2 = boto3.client('elbv2')
    tg_arn = create_target_group(elbv2, args)
    lb_arn = create_load_balancer(elbv2, args)
    create_listener(elbv2, tg_arn, lb_arn)


def create_target_group(elbv2, args):
    response = elbv2.create_target_group(**get_tg_parameters('tomcat-target-group', args.vpc_id))
    return response['TargetGroups'][0]['TargetGroupArn']


def create_load_balancer(elbv2, args):
    response = elbv2.create_load_balancer(**get_lb_parameters('tomcat-elbv2', args.subnet1, args.subnet2, args.sg))
    return response['LoadBalancers'][0]['LoadBalancerArn']


def create_listener(elbv2, tg_arn, lb_arn):
    elbv2.create_listener(**get_listener_parameters(tg_arn, lb_arn))


def get_listener_parameters(tg_arn, lb_arn):
    return {
        'LoadBalancerArn': lb_arn,
        'Protocol': 'HTTP',
        'Port': 80,
        'DefaultActions': [
            {
                'Type': 'forward',
                'TargetGroupArn': tg_arn,
            },
        ]

    }


def get_lb_parameters(name, subnet1, subnet2, security_group):
    return {
        'Name': name,
        'Subnets': [
            subnet1, subnet2,
        ],
        'SecurityGroups': [
            security_group,
        ],
        'Type': 'application',
        'IpAddressType': 'ipv4'
    }


def get_tg_parameters(name, vpc_id, port=8080, protocol='HTTP', health_check_port='8080', health_check_path='/'):
    return {
        'Name': name,
        'Protocol': protocol,
        'Port': port,
        'VpcId': vpc_id,
        'HealthCheckProtocol': protocol,
        'HealthCheckPort': health_check_port,
        'HealthCheckPath': health_check_path,
        'TargetType': 'ip'
    }


if __name__ == '__main__':
    main()

