# Natter (RouterOS优化版)

## 项目概述

本版本是对[原始Natter项目](https://github.com/MikeWang000000/Natter)的RouterOS功能增强优化版本，特别针对RouterOS设备进行了多项改进。

## 主要优化内容

### RouterOS功能优化
- 针对[natter#92](https://github.com/MikeWang000000/Natter/issues/92)问题，RouterOS不支持设置upnp自动过期时间，支持了Router NAT模式
- 基于RouterOS REST API操作NAT
- 支持自定义实例ID，局域网内同时运行多个Natter实例时，通过实例ID区分nat
### Docker能力优化
- 支持`--no-docker-check`参数关闭host模式检查
- 关闭host模式检查后，natter和业务容器可以通过network_mode: "service:xxx"的方式共享网络空间以实现转发且尽可能不影响宿主机网络

## 快速使用

### 基本测试
同natter

### RouterOS模式
```bash
python3 natter.py -R --ros-ip 192.168.1.1 --ros-user admin --ros-pass your_password
```

### 常用RouterOS选项
```
-R                 启用RouterOS NAT模式
--ros-ip <address> RouterOS设备IP（默认：192.168.88.1）
--ros-user <user>  登录用户名（默认：admin）
--ros-pass <pass>  登录密码
--ros-interface <if> 外网接口名称（可选，自动检测）
--ros-instance-id <id> 实例唯一标识
--no-docker-check  跳过Docker网络检查
```

## 原始项目
基于[https://github.com/MikeWang000000/Natter](https://github.com/MikeWang000000/Natter)项目改进

