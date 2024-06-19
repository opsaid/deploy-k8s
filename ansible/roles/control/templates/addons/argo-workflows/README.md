# argo-workflows

## 来源

https://github.com/argoproj/argo-workflows/tree/v3.5.8/manifests

## 制作方式

```shell
git clone --branch v3.5.8 --depth 1 https://github.com/argoproj/argo-workflows.git
```

```shell
cd argo-workflows/manifests/cluster-install
kustomize build > install.yaml
```
