import os
import yaml

def add_mappings_to_yaml(file_path, new_mappings):
    with open(file_path) as file:
        data = yaml.safe_load(file)

    # Check if 'destination' is 'hub-spot-test-account' and 'object' is 'contacts'
    if data.get('destination') == 'hub-spot-test-account' and data.get('config', {}).get('object') == 'contacts':
        if 'mappings' in data.get('config', {}):
            data['config']['mappings'].extend(new_mappings)
        else:
            data.setdefault('config', {}).setdefault('mappings', []).extend(new_mappings)

        with open(file_path, 'w') as file:
            yaml.safe_dump(data, file)

def process_folder(folder_path):
    new_mappings = [
        {'to': 'ht_last_sync_id', 'type': 'variable', 'variable': 'sync-id'},
        {'to': 'ht_sync_run_id', 'type': 'variable', 'variable': 'sync-run-id'},
        {'to': 'ht_last_sync_run_url', 'type': 'template', 'template': '>-https://app.hightouch.com/lauraweb-2023-dev/syncs/{{ context[\'sync_id\'] }}/runs/{{ context[\'sync_run_id\'] }}'}
    ]

    for filename in os.listdir(folder_path):
        if filename.endswith('.yaml') or filename.endswith('.yml'):
            file_path = os.path.join(folder_path, filename)
            add_mappings_to_yaml(file_path, new_mappings)

current_path = os.getcwd()
process_folder(current_path)