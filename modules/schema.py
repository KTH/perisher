__author__ = 'tinglev'

SCHEMA_ROOT = {
    "type": "object",
    "properties": {
        "clusters": {"type": "array"}
    },
    "required": ["clusters"]
}

SCHEMA_CLUSTER = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "vms": {"type": "array"},
        "lbs": {"type": "array"}
    },
    "required": ["name"]
}

SCHEMA_VM = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "private_ip": {"type": "string", "format": "ipv4"}
    },
    "required": ["name", "private_ip"]
}

SCHEMA_LB = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "private_ip": {"type": "string", "format": "ipv4"},
        "public_ip": {"type": "string", "formtat": "ipv4"},
        "fqdn": {"type": "string"}
    },
    "required": ["name"]    
}

SCHEMA_PROMETHEUS = {
    "type": "object",
    "properties": {
        "targets": {"type": "array"},
        "labels": {"type": "object"}
    },
    "required": ["targets", "labels"]
}
