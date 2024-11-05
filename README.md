
## 序

本项目发展自https://github.com/findmover/wxread，进行了docker容器化，使用环境变量和外置json来加载配置，减少修改次数和难度

## 脚本介绍

针对微信读书阅读挑战赛编写的脚本：

1. 能进行刷阅读时长，且时长默认计入排行榜、挑战赛等。（指定200分钟）
2. 可部署服务器每天定时运行脚本并推送到微信。
3. 一次抓包，长时间使用。对于Cookie更新问题给出了自动获取Cookie更新值的解决方案。
4. 比较市面上的ADB调试器、自动阅读器，本脚本实现了轻量化编写，部署服务器即可运行，无需更多环境条件。
5. 脚本JS逆向分析各接口请求，分析各字段的拼接方式，并对字段进行加密、计算处理使得服务器能够成功响应（`{'succ': 1, 'synckey': 2060028311}`，表示数据字段正常）。

## config.json获取步骤

1、在微信阅读官网 [微信读书 (qq.com)](https://weread.qq.com/) 搜索【三体】点开阅读点击下一页进行抓包，抓到`read`接口 `https://weread.qq.com/web/book/read`，如果返回格式正常（如：

```
json复制代码{
  "succ": 1,
  "synckey": 564589834
}
```

右键复制为Bash格式，然后在 [Convert curl commands to Python (curlconverter.com)](https://curlconverter.com/python/) 转化为Python脚本，复制需要的headers、cookies与data字段替换到`config.json`即可。

## 操作步骤

### 1. 下载并修改 `config.json`

首先，下载 `config.json` 文件，并根据需要进行修改。该文件包含了请求所需的 `data`、`headers` 和 `cookies` 信息。

### 2. 使用 Docker 运行

使用以下命令运行 Docker 容器，并挂载 `config.json` 文件：

```sh
docker run -d --name weread-bot 
  -v /PATH/TO/config.json:/app/config.json \
  -e READ_COUNT=120 \
  -e PUSH_METHOD=none \
  hypered1/weread-bot:latest
```
可使用`docker logs -s weread-bot`查看日志输出
### 3、Pushplus/telegram推送，更改你的环境变量和Token即可。

## 环境变量

READ_COUNT: 设置阅读次数，每次阅读 30 秒，默认值为 200，即 100 分钟。
PUSH_METHOD: 设置推送方式，可选值为 none、pushplus、telegram。默认值为 none。
PUSHPLUS_TOKEN: 如果使用 PushPlus 推送，需要设置此环境变量为您的 PushPlus Token。
TG_BOT_TOKEN: 如果使用 Telegram 推送，需要设置此环境变量为您的 Telegram Bot Token。
TG_CHAT_ID: 如果使用 Telegram 推送，需要设置此环境变量为您的 Telegram Chat ID。
CONFIG_PATH: 配置文件路径，默认为 /app/config.json。

### 字段解释

- `appId`: `"wbxxxxxxxxxxxxxxxxxxxxxxxx"` ✔
  - 应用的唯一标识符。

- `b`: `"ce032b305a9bc1ce0b0dd2a"` ✔
  - 书籍或章节的唯一标识符。

- `c`: `"0723244023c072b030ba601"` ✔
  - 内容的唯一标识符，可能是页面或具体段落。

- `ci`: `60` ✔
  - 章节或部分的索引。

- `co`: `336` ✔
  - 内容的具体位置或页码。

- `sm`: `"[插图]威慑纪元61年，执剑人在一棵巨树"` ✔
  - 当前阅读的内容描述或摘要。

- `pr`: `65` ✔
  - 页码或段落索引。

- `rt`: `88` ✔
  - 阅读时长或阅读进度。

- `ts`: `1727580815581` ✔
  - 时间戳，表示请求发送的具体时间（毫秒级）。

- `rn`: `114`
  - 随机数或请求编号，用于标识唯一的请求。

- `sg`: `"bfdf7de2fe1673546ca079e2f02b79b937901ef789ed5ae16e7b43fb9e22e724"`
  - 安全签名，用于验证请求的合法性和完整性。

- `ct`: `1727580815` ✔
  - 时间戳，表示请求发送的具体时间（秒级）。

- `ps`: `"xxxxxxxxxxxxxxxxxxxxxxxx"` ✔
  - 用户标识符或会话标识符，用于追踪用户或会话。

- `pc`: `"xxxxxxxxxxxxxxxxxxxxxxxx"` ✔
  - 设备标识符或客户端标识符，用于标识用户的设备或客户端。

- `s`: `"fadcb9de"`
  - 校验和或哈希值，用于验证请求数据的完整性。
