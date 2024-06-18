# argo-cd

## 来源

https://github.com/argoproj/argo-cd/tree/v2.11.3/manifests

## 制作方式

```shell
git clone --branch v2.11.3 --depth 1 https://github.com/argoproj/argo-cd.git
```

```shell
cd argo-cd/manifests/crds
kustomize build > crds.yaml
```

## 相关特性

1. 移除内置 dex 服务，不支持 "dex.config" 配置；
