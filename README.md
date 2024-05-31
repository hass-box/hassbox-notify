# HassBox 通知报警

可将报警信息发送到你的微信，支持短信和电话语音。紧急报警推荐使用电话语音！

## 安装/更新

#### 方法 0: 联系客服安装

啥也不会的小白，可以至 HassBox 微信公众号联系客服，我们免费远程帮你安装！

#### 方法 1: 通过`Samba`或`SFTP`手动安装

下载`hassbox_notify.zip`并解压，复制`hassbox_notify`文件夹到 Home Assistant 根目录下的`custom_components`文件夹中。

#### 方法 2: 通过`SSH`或`Terminal & SSH`加载项执行一键安装命令

```shell
curl -fsSL get.hassbox.cn/hassbox-notify | bash
```

#### 方法 3: 通过`shell_command`服务

1. 复制下面的代码到 Home Assistant 配置文件`configuration.yaml`中

   ```yaml
   shell_command:
     update_hassbox_notify: |-
       curl -fsSL get.hassbox.cn/hassbox-notify | bash
   ```

2. 重启 Home Assistant

3. 在 Home Assistant 开发者工具中调用此服务[`service: shell_command.update_hassbox_notify`](https://my.home-assistant.io/redirect/developer_call_service/?service=shell_command.update_hassbox_notify)

## 使用教程
