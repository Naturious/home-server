# Home Server

Ansible playbooks for setting up a home server.

## Usage

Install Ansible:

```bash
brew install ansible
```


Deploy the playbooks to the target host:

```bash
ansible-playbook -i inventories/hosts.ini playbooks/jellyfin.yml -K
```
