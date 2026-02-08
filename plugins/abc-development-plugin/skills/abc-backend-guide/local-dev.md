# 本地开发环境指南

> 后端项目本地开发的环境配置说明。

## 1. 环境准备

| 软件 | 版本要求 | 安装方式 |
|------|---------|---------|
| JDK | 1.8 | `brew install openjdk@8` |
| Gradle | 项目自带 wrapper，版本因项目而异 | 不需要单独安装 |

## 2. 环境配置（Profile）

后端项目通过 **Profile** 区分环境：

| Profile | 配置文件 | 连接环境 | 说明 |
|---------|---------|---------|------|
| `local` | `bootstrap-local.yml` | dev 开发环境 | **固定存在**，本地开发默认使用 |
| `local-test` | `bootstrap-local-test.yml` | test 测试环境 | **可能不存在**，本地直连测试环境 |
| `docker` | `bootstrap-docker.yml` | 由环境变量决定 | 容器部署用 |

**切换环境**：
```bash
# 本地开发（连接 dev 环境）
./gradlew bootRun --args='--spring.profiles.active=local'

# 本地直连测试环境（如果有 local-test profile）
./gradlew bootRun --args='--spring.profiles.active=local-test'
```

## 3. 如何查看端口号

端口配置在 `bootstrap.yml` 或 `bootstrap-local.yml` 中：

```yaml
server:
  port: 18888   # ← 这就是端口号
```

## 4. Gradle 常用命令

```bash
# 下载依赖并编译
./gradlew build

# 启动开发服务器
./gradlew bootRun --args='--spring.profiles.active=local'

# 只编译不运行（检查代码是否有编译错误）
./gradlew compileJava

# 清理构建产物
./gradlew clean

# 查看依赖树
./gradlew dependencies
```
