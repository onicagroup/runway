"""
This type stub file was generated by pyright.
"""

import os

if os.getenv("TROPO_REAL_BOOL") in ["1", "true", "True"]:
    def boolean(x): ...

else:
    def boolean(x): ...

def integer(x): ...
def positive_integer(x): ...
def integer_range(minimum_val, maximum_val): ...
def integer_list_item(allowed_values): ...
def double(x): ...
def ignore(x):
    """Method to indicate bypassing property validation"""
    ...

def defer(x):
    """Method to indicate defering property validation"""
    ...

def network_port(x): ...
def tg_healthcheck_port(x): ...
def s3_bucket_name(b): ...
def elb_name(b): ...
def encoding(encoding): ...
def status(status): ...
def s3_transfer_acceleration_status(value): ...
def iam_names(b): ...
def iam_user_name(user_name): ...
def iam_path(path): ...
def iam_role_name(role_name): ...
def iam_group_name(group_name): ...
def one_of(class_name, properties, property, conditionals): ...
def mutually_exclusive(class_name, properties, conditionals): ...
def exactly_one(class_name, properties, conditionals): ...
def check_required(class_name, properties, conditionals): ...
def json_checker(prop): ...
def notification_type(notification): ...
def notification_event(events): ...
def task_type(task): ...
def compliance_level(level): ...
def operating_system(os): ...
def vpn_pre_shared_key(key): ...
def vpn_tunnel_inside_cidr(cidr): ...
def vpc_endpoint_type(endpoint_type): ...
def scalable_dimension_type(scalable_dimension): ...
def service_namespace_type(service_namespace): ...
def statistic_type(statistic): ...
def key_usage_type(key): ...
def cloudfront_event_type(event_type): ...
def cloudfront_viewer_protocol_policy(viewer_protocol_policy): ...
def cloudfront_restriction_type(restriction_type): ...
def cloudfront_forward_type(forward): ...
def cloudfront_cache_cookie_behavior(cookie_behavior): ...
def cloudfront_cache_header_behavior(header_behavior): ...
def cloudfront_cache_query_string_behavior(query_string_behavior): ...
def cloudfront_origin_request_cookie_behavior(cookie_behavior): ...
def cloudfront_origin_request_header_behavior(header_behavior): ...
def cloudfront_origin_request_query_string_behavior(query_string_behavior): ...
def priceclass_type(price_class): ...
def ecs_proxy_type(proxy_type): ...
def backup_vault_name(name): ...
def waf_action_type(action): ...
def resourcequery_type(type): ...
def storage_type(storage_type): ...
def canary_runtime_version(runtime_version): ...
def component_platforms(component_platform): ...
def imagepipeline_status(status): ...
def schedule_pipelineexecutionstartcondition(startcondition): ...
def ebsinstanceblockdevicespecification_volume_type(type): ...
def containerlevelmetrics_status(status): ...
def accelerator_ipaddresstype(type): ...
def listener_clientaffinity(affinity): ...
def listener_protocol(protocol): ...
def endpointgroup_healthcheckprotocol(protocol): ...
def session_findingpublishingfrequency(frequency): ...
def session_status(status): ...
def findingsfilter_action(action): ...
def ecs_efs_encryption_status(status): ...
