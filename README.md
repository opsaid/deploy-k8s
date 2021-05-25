# 最小化准生产环境k8s部署

k8s生态同类功能的可选组件太多，本项目在于结合自身经验对各个组件做精简整合

## 如何部署

- 更改变量

```
mv ansible/hosts_sample.ini ansible/hosts.ini
vim ansible/hosts.ini
```

- 生成证书

```
ansible-playbook -i hosts.ini deploy.yaml -t pki
```

- 部署集群

```
ansible-playbook -i hosts.ini deploy.yaml -t common,control,worker
```

- 验证集群

登录node1节点

```
kubectl get cs
```

如果存在不为"ok"的服务，则需检查，如果正常，则创建以下基础服务

```
kubectl apply -f /usr/local/src/manifests/rbac.yaml
kubectl apply -f /usr/local/src/manifests/psp.yaml
kubectl apply -f /usr/local/src/manifests/metrics-server.yaml
kubectl apply -f /usr/local/src/manifests/coredns.yaml
kubectl apply -f /usr/local/src/manifests/calico.yaml
```

- 认证节点

登录node1节点

```
for i in $(kubectl get csr | grep -v NAME | awk '{ print $1 }'); do kubectl certificate approve $i; done
```
