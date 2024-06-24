# dex

## 来源

https://github.com/dexidp/helm-charts/tree/dex-0.18.0

## 制作方式

```shell
git clone --branch dex-0.18.0 --depth 1 https://github.com/dexidp/helm-charts.git
```

```shell
cd helm-charts/charts/
helm template --release-name dexidp --namespace kube-system dex --set grpc.enabled=true
```
