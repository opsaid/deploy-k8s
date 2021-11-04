# deploy k8s

k8s生态组件过多，对新人入门并不友好，本项目在于结合当前生产集群维护经验，总结一套标准的部署模版，接入内部gitlab ci实现集群基础设施的自动化管理发布，同时也会不断迭代优化部署模版，以实现快速搭建一套生产可用的环境。

主要实现以下三个目标：

1. 基于gitlab实现对集群基础设施的管理
2. 集群同类组件只选其一，不会给予多种选择
3. 提供部署的标准化架构，之后个性化在各自仓库做定制

***当前还在开发优化中***

## 依赖环境

操作系统：centos7 2u4g

## 如何使用

### 初始化部署脚本准备

- 拷贝部署代码

```
git clone https://github.com/opsaid/deploy-k8s.git
```

里面包含环境所需的二进制文件（通过git lfs管理，所以客户端也需要支持该特性），下载可能需要点时间。

- 清理git

```
cd deploy-k8s
rm -rf .git
```

模版下载完成后，原先git的记录可以删除，因为之后会基于该模版导入各自内部仓库。

- 更改变量

```
mv ansible/hosts_sample.ini ansible/hosts.ini
mv ansible/group_vars/all_sample.yaml ansible/group_vars/all.yaml
mv ansible/group_vars/control_sample.yaml ansible/group_vars/control.yaml
```

其中ansible/hosts.ini、ansible/group_vars/all.yaml之中的参数根据环境做更改。

### 通过gitlab执行

- gitlab runner准备

TODO

- 导入内部gitlab仓库

```
git init
git remote add origin http://{GIT_REPO}

git add .
git commit -m "Initial commit"
git push -u origin master
```

变量GIT_REPO，对应内部的gitlab仓库地址。

- 查看部署过程

登录gitlab CI/CD页面查看部署过程

### 通过本地手工执行

确保本地可以ssh免密登录hosts.ini中登记的主机地址。

- 生成证书

```
ansible-playbook -i hosts.ini deploy.yaml -t pki
```

- 部署集群

```
ansible-playbook -i hosts.ini deploy.yaml -t common,control,worker
```

### 验证集群

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

## Others

debian11默认使用cgroup v2，会导致kubelet启动不了，这里降级使用cgroup v1版本

```
/etc/default/grub

GRUB_CMDLINE_LINUX="systemd.unified_cgroup_hierarchy=0"
```

```
grub-mkconfig -o /boot/grub/grub.cfg
```

