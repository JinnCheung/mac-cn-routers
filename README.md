mac-cn-routers
=========

此python脚本主要是对[chnroutes]脚本的更新和优化，让VPN跳过国内网站，只支持MacOS系统。

## 环境

1. 系统：MacOS.
2. 框架：python3.
3. 依赖：requests.

## 用法

```shell
python3 mac-cn-ip.py
```

## 其他

为了让VPN跳过国内网站，参考了几个现成方案

- [chnroutes] 拉取 [APNIC Delegated List], 整理出国内IP，然后生成`ip-up`和`ip-down`两个脚本，需自行复制到`/etc/ppp/`。

- [ppp] 直接把mac版的`ip-up`和`ip-down`两个文件给放出来了。

- [chnroutes2] 通过CN2路由定期获取国内ip表。

本脚本拉取[chnroutes2]的数据，参考[chnroutes]生成`ip-up`和`ip-down`两个脚本，自动复制到`/etc/ppp/`。

[chnroutes]: https://github.com/fivesheep/chnroutes
[ppp]: https://github.com/alsotang/ppp
[chnroutes2]: https://github.com/misakaio/chnroutes2