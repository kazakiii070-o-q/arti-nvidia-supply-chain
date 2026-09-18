# NVIDIA 供应链与合作关系研究服务

基于公开可访问资料构建的 **NVIDIA 供应链与公司关系研究数据集 + HTTP JSON API + CLI**。

本项目用于展示如何将企业公开披露中的供应商、客户/部署关系、合作伙伴、投资关系及同行关系，整理为**可追溯、可复核、可运行**的结构化研究数据。

> **研究截止时间：2026-09-18**

## 一、研究对象与范围

- **研究对象：** NVIDIA Corporation
- **证券标识：** NASDAQ: NVDA
- **研究截止时间：** 2026-09-18
- **关系范围：**
  - supplier：供应商
  - customer / documented_deployment_relationship：客户或有公开证据支持的部署关系
  - partner：合作伙伴
  - investor / investee：投资方或被投方关系
  - peer：同行/竞争关系
- **资料范围：** SEC 披露、NVIDIA 官方公告及合作方/交易对手方公开披露等合法可访问资料。
- **明确排除：** 登录后内容、付费墙、验证码绕过、robots/访问限制绕过、API Key、个人数据、客户机器或其他受限制数据。

本项目区分：

1. **confirmed：** 公开来源对关系有较直接、明确的支持；
2. **documented_deployment_relationship / documented_lease_relationship：** 有公开部署、租赁或基础设施合作证据，但不足以直接断言传统意义上的“直接客户”；
3. **unknown：** 公开资料不足以确认的部分，不用推测填充。

## 二、为什么采用保守的关系判定

企业之间出现合作、采购、部署或技术集成，并不意味着双方一定存在传统意义上的“客户关系”。

例如，NVIDIA 的 SEC 文件对 direct customers 与 indirect customers 有明确区分。因此，本项目不会因为某家公司使用 NVIDIA GPU、参加联合发布或出现在基础设施项目中，就直接把该公司标记为“直接客户”。

这种处理方式的目标不是让数据看起来很完整，而是让 reviewer 能够从**关系结论 → 证据 → 原始来源**逐层回溯。

## 三、数据字段与证据链

每条关系至少包含以下研究信息：

- source_company：关系发起/研究主体
- target_company：关系对象
- relationship_type：关系类型
- direction：关系方向
- status：关系状态
- confidence：0-100 的证据置信度
- evidence：证据来源及定位信息
- publication_date：来源发布日期
- access_date：研究访问日期
- source_url：原始来源 URL
- evidence_locator：页码、章节、公告标题或其他定位信息
- access_limitations：访问或许可限制说明
- notes：关系判定说明、时间状态及必要的谨慎解释

置信度并非“投资价值评分”，而是对**关系证据质量**的量化表达，主要考虑：

- 来源权威程度
- 是否为第一方/独立来源
- 证据是否直接支持该关系
- 时效性
- 关系类型是否明确
- 是否存在定量信息
- 是否存在来源冲突或歧义

## 四、当前研究结果

当前数据集包含 **35 条关系记录**，覆盖挑战要求的主要关系类别：

- 供应商
- 客户/公开部署关系
- 合作伙伴
- 投资关系
- 同行/竞争关系

典型关系包括：

- NVIDIA → TSMC：供应关系
- NVIDIA → Samsung Electronics：供应关系
- NVIDIA → SK hynix：供应关系
- NVIDIA → Micron Technology：供应关系
- NVIDIA → Marvell Technology：合作及投资关系
- NVIDIA → Meta：AI 基础设施合作/部署关系
- NVIDIA → Microsoft：AI PC/平台合作关系
- NVIDIA → AMD、Intel：同行/竞争关系

完整数据位于 `data/relationships.json`。

## 五、主要证据来源

项目优先使用企业及监管机构的一手公开资料，包括：

- NVIDIA SEC 10-K / 10-Q
- NVIDIA 官方新闻稿
- 合作方官方公告
- SEC Exhibit / 公司监管披露

部分核心来源包括 NVIDIA FY2026 10-K、FY2027 Q2 10-Q，以及 NVIDIA 与 AWS、Marvell、MediaTek、Meta、Microsoft、Palantir、Coherent 等公司的公开公告。

每条关系均在数据中保留对应来源 URL 和 evidence locator，避免只给出一个无法复核的结论。

## 六、项目结构

```text
data/
└── relationships.json       # 主研究数据集

fixtures/
└── sample_relationships.json # 可重复运行的测试数据

docs/
└── evidence-policy.md       # 证据判定规则与研究方法

src/
├── api.py                   # HTTP JSON API
├── cli.py                   # CLI 命令行入口
└── __init__.py

scripts/
└── validate_data.py         # 数据字段与 URL 校验

tests/
├── test_data.py             # 主数据测试
└── test_fixture.py          # fixture 测试

requirements.txt             # Python 依赖
README.md                    # 项目说明与复现方法
```

## 七、环境与启动

### 1. 创建虚拟环境

```bash
python -m venv .venv
```

Windows：

```bash
.venv\Scripts\activate
```

macOS / Linux：

```bash
source .venv/bin/activate
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 校验研究数据

```bash
python scripts/validate_data.py
```

### 4. 运行测试

```bash
pytest
```

### 5. 启动 HTTP API

```bash
uvicorn src.api:app --reload
```

## 八、HTTP JSON API

### 健康检查

```text
GET /health
```

### 数据摘要

```text
GET /summary
```

### 查询 NVIDIA 的全部关系

```text
GET /companies/NVIDIA/relationships
```

### 按关系类型筛选

```text
GET /companies/NVIDIA/relationships?type=supplier
```

### 查询指定公司相关关系

```text
GET /relationships/Marvell%20Technology
```

API 返回 JSON，可用于后续关系图、研究工作台或 AI 分析服务。

## 九、CLI 命令行入口

查询供应商：

```bash
python -m src.cli --type supplier
```

查询指定公司：

```bash
python -m src.cli --target "Marvell Technology"
```

以 JSON 输出投资关系：

```bash
python -m src.cli --type investor --json
```

## 十、数据更新与复现

数据更新遵循以下流程：

```text
公开资料检索
    ↓
确认企业实体与关系方向
    ↓
提取原始证据与时间信息
    ↓
判断关系类型及证据强度
    ↓
记录 source URL + evidence locator
    ↓
写入 relationships.json
    ↓
运行 validate_data.py
    ↓
运行 pytest
    ↓
提交 GitHub
```

`fixtures/sample_relationships.json` 用于提供稳定的最小数据样本，使 reviewer 不需要重新抓取互联网数据即可验证 API/CLI 的基本行为。

## 十一、关键路径与边界测试

关键路径：

```text
data/relationships.json
        ↓
src/api.py / src/cli.py
        ↓
HTTP JSON / CLI 查询
```

已覆盖的基础边界包括：

- 必填字段缺失检测
- URL 格式检测
- 非法 relationship type 检测
- fixture 数据的确定性测试
- NVIDIA 关系记录的数据完整性检查

## 十二、已知限制

1. 本项目不是全网供应链数据库，数据规模有意控制在可追溯范围内。
2. 企业关系可能在研究截止时间之后发生变化，因此数据带有明确时间边界。
3. 部分企业之间存在合作、部署、租赁、投资等多重关系，不能简单归类为单一“客户关系”。
4. 公开披露存在选择性披露问题，未找到公开证据不代表关系一定不存在。
5. 不同来源可能存在发布时间、实体名称或关系描述差异，因此项目保留原始来源和谨慎说明，而不是强行统一成确定结论。
6. 后续如果扩展到更大规模数据，需要进一步增加实体消歧、来源去重、历史版本、关系失效时间以及自动化更新机制。

## 十三、AI / Coding Agent 使用说明

本项目可以使用 AI 或 Coding Agent 辅助完成以下工作：

- 研究资料初步整理
- 数据字段设计
- API / CLI 代码生成与调试
- 测试用例生成
- README 文档整理

AI 仅作为辅助工具，关系判断、证据核验、研究口径以及最终工程交付由人工负责。

项目过程中不上传或处理 API Key、个人敏感信息、客户机器数据、受限制数据或需要绕过访问控制才能取得的资料。

## 十四、项目定位

本项目的目标不是直接回答“NVDA 值不值得投资”，而是建立一个能够支持进一步投资研究的**可追溯关系数据层**：

```text
公开证据
   ↓
结构化关系
   ↓
证据置信度
   ↓
关系查询 / 关系图
   ↓
进一步的公司与产业链研究
```

最终希望 reviewer 可以从任意一条关系记录出发，定位到具体来源，理解为什么建立该关系、关系方向是什么、证据强度如何，以及哪些地方仍然存在未知或不确定性。

## 十五、人工采编流程
1. 以 NVIDIA 最近10-K/10-Q 为种子，提取 foundry/memory/packaging/assembly/substrate 点名实体。
2. 对每个候选实体单独检索：NVIDIA IR新闻、对手方年报/互动易/招股书、交易所公告；不接受仅券商研报的关系。
3. 每条关系记录 publisher、publication_date、source_url、evidence_locator、原文摘录；按 evidence-policy 定 L1-L3 与 confidence。
4. 区分 direct/indirect customer：仅当披露显示直接采购/ODM/OEM/分销才标 direct，其余标 deployment/partner。
5. 疑似关系（如A股仅称“AI服务器材料”、无NVIDIA点名）放入 data/relationships_unconfirmed.json，不进主评。
6. 全部数据跑 validate_data.py + pytest；结果附本文件。
7. AI仅用于生成模板/初筛关键词，最终录入由人工核对原文后确定。



