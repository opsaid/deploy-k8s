## 概览

k8s生态组件过多，对新人入门并不友好，本项目在于结合当前生产集群维护经验，总结一套标准的部署模版，接入内部gitlab ci实现集群基础设施的自动化管理，同时也会不断迭代优化，以实现快速搭建一套生产可用的环境。

## 前置说明

### 操作系统

操作系统支持：centos 7 或者 ubuntu 20.04

- centos 7

通过"CentOS-7-x86_64-Minimal-2009.iso"镜像做最小化安装

- ubuntu 20.04

选择最小化，同时安装sshd服务

### 主机拓扑

角色 | 建议数量 | CPU架构 | 示例IP
--------|-------|-------|---------
[ansible中控](/docs/deploy-k8s/quickstart/#ansible中控) | 1  | amd64 | 192.168.31.200
[负载均衡器](/docs/deploy-k8s/quickstart/#负载均衡器) | 至少1 | amd64 | 192.168.31.200
[k8s控制节点](/docs/deploy-k8s/quickstart/#部署控制平面) | 1、3、5 | amd64 | 192.168.31.201/202/203
[k8s工作节点](/docs/deploy-k8s/quickstart/#新增工作节点) | 至少1 | amd64 | 192.168.31.204

中控必须配置好免密ssh登录其他节点，如果仅用于部署测试负载均衡器可与中控共用，生产环境负载均衡器必须至少2节点且支持VIP。

## 环境部署

### ansible中控

在中控执行以下步骤：

- 安装基础软件

centos7

```shell
yum install -y epel-release
yum install -y git ansible
```

ubuntu20.04

```shell
apt install -y git ansible
```

- 获取部署代码

```shell
git clone https://github.com/opsaid/deploy-k8s.git
```

- 配置ssh免密登录

```shell
ssh-copy-id -p 22 root@192.168.31.20X
```

### 负载均衡器

TODO

## 部署控制平面

### 步骤1：首次初始化配置修改

- 必须更改的文件

```shell
ansible/hosts.ini
ansible/group_vars/all.yaml
```

- 可选更改的文件

```shell
ansible/group_vars/default.yaml
ansible/group_vars/component-v1.18.yaml
ansible/group_vars/component-v1.22.yaml
```

选择component-v1.18或compoent-v1.22是由选择部署的k8s版本所决定

### 步骤2：下载依赖的二进制文件

方式1：预先下载安装包（推荐）

二进制文件包与镜像包

```shell
https://github.com/opsaid/deploy-k8s/releases
```

方式2：在线下载构建

```shell
# 由于网络原因，需要代理HTTPS可以配置下加速通道传输（127.0.0.1:1087仅为示例）
#export HTTPS_PROXY=http://127.0.0.1:1087

yum install -y docker
systemctl start docker

# 编译制作 pause 镜像需要
yum install -y gcc glibc-static

ansible-playbook -i hosts.ini deploy.yaml -t binary
```

### 步骤3：生成集群依赖证书

```shell
ansible-playbook -i hosts.ini deploy.yaml -t pki
```

### 步骤4：系统公共组件安装

```shell
ansible-playbook -i hosts.ini deploy.yaml -t common
```

>> 确保主机节点已在`host.ini`配置项`[kube_control_plane]`中

### 步骤5：部署控制平面节点

```shell
ansible-playbook -i hosts.ini deploy.yaml -t control
```

>> 确保主机节点已在`host.ini`配置项`[kube_control_plane]`中

### 步骤6：验证控制平面组件

登录任一控制节点，查看关键组件的运行状态（可能需等待一段时间）

- 通过 `crictl` 查看本节点容器

```shell
crictl ps
```

其中"kube-apiserver"、"kube-controller-manager"、"etcd"、"kube-scheduler"组件，必须是"Running"状态。

- 通过 `kubectl` 查看所有节点容器

```shell
kubectl get pods -n kube-system
```

其中"kube-apiserver"、"kube-controller-manager"、"etcd"、"kube-scheduler"组件，在各节点必须是"Running"状态。

### 步骤7：部署集群基础组件

登录任意一个控制平面节点，部署addons

```shell
kustomize build /usr/local/src/addons/calico/ | kubectl apply -f -
kustomize build /usr/local/src/addons/coredns/ | kubectl apply -f -
kustomize build /usr/local/src/addons/kube-proxy/ | kubectl apply -f -
kustomize build /usr/local/src/addons/kube-system/ | kubectl apply -f -
kustomize build /usr/local/src/addons/metrics-server/ | kubectl apply -f -
```

>>如在使用k8s v1.22也可直接使用```kubectl apply -k```代替```kustomize```

### 步骤8：控制平面相关维护

TODO

## 新增工作节点

### 步骤1：在ansible的`host.ini`中添加节点

```shell
[all]
......
node4 ansible_host=192.168.31.204 ansible_port=22 ip=192.168.31.204

[kube_node]
......
node4
```

### 步骤2：ansible中控节点可ssh节点

```shell
$HOME/.ssh/authorized_keys
```

### 步骤3：系统公共组件安装

```shell
ansible-playbook -i hosts.ini deploy.yaml -t common
```

### 步骤4：添加集群工作节点

```shell
ansible-playbook -i hosts.ini deploy.yaml -t worker
```

### 步骤5：验证允许节点加入

- 查看节点加入请求

```shell
kubectl get csr
```

其中"CONDITION"="Pending"状态；

- 授权制定节点的加入

```shell
kubectl certificate approve ${node-csr-XXXX}
```

- 等待节点加入并状态为可用

```shell
kubectl get nodes
```

>>在任一控制平面节点执行

## 完成验收与后续

TODO
