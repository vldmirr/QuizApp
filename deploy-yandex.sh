#!/bin/bash

# Create Yandex Cloud instance
yc compute instance create \
  --name fastapi-app \
  --zone ru-central1-a \
  --network-interface subnet-name=default,nat-ip-version=ipv4 \
  --memory 4 \
  --cores 2 \
  --create-boot-disk image-folder-id=standard-images,image-family=ubuntu-2004-lts \
  --ssh-key ~/.ssh/id_rsa.pub

# Get instance IP
INSTANCE_IP=$(yc compute instance get fastapi-app --format json | jq -r '.network_interfaces[0].primary_v4_address.one_to_one_nat.address')

# Deploy with Ansible
ansible-playbook -i "${INSTANCE_IP}," ansible/playbook.yaml -u ubuntu