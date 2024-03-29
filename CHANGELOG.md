# 1 更新日志

基于二进制的最小化准生产环境k8s部署

## Unreleased

## v2.2.0 - [2022-12-11]

### Added

- kubeconfig 相关文件证书更改为内嵌

1. 对文件admin.conf 更改证书路径为 base64 的内容
2. 兼容 kubeadm certs check-expiration 查看证书过期时间

- 自定义 ca 与成员证书的有效时间

1. ansible/group_vars/default.yaml 新增 "ca_expiry_days" 表示ca过期天数

- 添加 ingress-nginx 的 addons

1. 支持 k8s 1.22 版本添加 ingress-nginx addons

- 更改 k8s 1.18 镜像名称风格

1. 由原先 {{ internal_images.system.kube_proxy }}-{{ server_arch }} 调整为 {{ internal_images.system.kube_proxy }} 不在使用系统架构为后缀，如：amd64

## v2.1.1 - [2022-05-25]

### Added

- containerd配置适配1.5版本优化
- 添加kata-containers支持

## v2.1.0 - [2022-03-06]

### Added

- 重构部署，控制平面基于静态POD方案

## v0.1.3 - [2021-12-07]

### Fixed

- 开启calico felix http健康检测服务

### Added

- 进程以普通用户运行代替root
- 禁用calico的bird6
- calico滚动更新更改为OnDelete
- 支持管理与业务网段的配置
- 调整kubelet安装目录以符合kubeadm规范

## v0.1.1 - [2021-11-02]

### Added

- 新增系统级别是否禁用ipv6选项
- 可控制关键进程coredns、calico controller是否必须部署在管理节点
- debian11默认使用cgroup v2，kubelet当前依赖v1，在grub配置使用v1版本

## v0.1.0 - [2021-03-26]

### Added

- 初版提交

# 2 格式说明

名称 | 说明
------|----------
Fixed | 功能的修复
Added | 添加新功能
Changed    | 功能的变更
Security   | 有关安全问题的Bug修复
Deprecated | 不建议使用，未来可能会删除
Removed    | 之前为Deprecated状态，此版本被移除
