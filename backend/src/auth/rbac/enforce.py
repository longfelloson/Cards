import casbin

MODEL_CONFIG_PATH = "../rbac-model.conf"
POLICY_CONFIG_PATH = "../rbac-policy.csv"

ENFORCER = casbin.Enforcer(MODEL_CONFIG_PATH, POLICY_CONFIG_PATH)
