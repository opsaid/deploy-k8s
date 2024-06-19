# argo-events

## 来源

https://github.com/argoproj/argo-events/tree/v1.9.2/manifests

## 制作方式

```shell
git clone --branch v1.9.2 --depth 1 https://github.com/argoproj/argo-events.git
```

```shell
cd argo-events/manifests/cluster-install
kustomize build > install.yaml
```

```shell
cd argo-events/manifests/extensions/validating-webhook
kustomize build > events-webhook.yaml
```
