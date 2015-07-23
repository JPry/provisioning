# JPry custom provisioning

[Ansible](http://www.ansible.com/home) is a wonderful tool for automating system maintenance and configuration. I've decided to use it for my personal computers to keep my tools consistent everywhere. To get started, clone this repo to a machine that already has ansible installed, then run the playbook:

```
ansible-playbook -i inventory/hosts provision.yml
```

**Note:** Requires Ansible 2.0.0 or greater.
