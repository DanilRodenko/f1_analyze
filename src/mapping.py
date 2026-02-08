from config.dnf_groups import DNF_GROUPS, STATUS_FINISHED

def dnf_status_mapping(df):
    dnf_mapping = {}
    for group_name, ids in DNF_GROUPS.items():
        for s_id in ids:
            dnf_mapping[s_id] = group_name

    df['dnfStatus'] = df['status'].map(dnf_mapping)


def status_mapping(df):
    status_mapping = {}
    for group_name, ids in STATUS_FINISHED.items():
        for s_id in ids:
            status_mapping[s_id] = group_name
    df['statusGroup'] = df['statusId'].map(status_mapping)
