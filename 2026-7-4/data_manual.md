# AI岗位需求能力分析 - 数据使用手册

---

## 一、项目概览

本项目从招聘JD（Job Description）原始数据出发，经过 **清洗 → 抽取 → 分析 → 导出** 四步流水线，产出面向 ECharts 前端可视化的结构化数据，用于构建 **AI岗位需求能力图谱**。

### 核心解决的问题

| 问题 | 解决机制 |
|------|----------|
| JD数据"时滞"（过期招聘信息） | 指数衰减权重 `exp(-0.008 × 天数)`，update_date 自动映射为 publish_date |
| JD数据"噪音"（抄袭/通胀） | MinHash+LSH去重 + 同源批量惩罚 + 技能堆砌检测 |
| JD文本脏数据（转义符/前缀噪声） | 全局清洗：去转义引号、冗余前缀、残留冒号、末尾噪声 |
| 岗位名含待遇噪声 | clean_job_title() 自动剥离"朝九晚六""双休""五险一金"等待遇词 |
| 能力"幻觉"（虚假技能关联） | 词典校验(40%) + 白皮书认证(20%) + 多源交叉验证(40%) |
| 置信度无区分度 | 无 source 时根据公司名推断来源权重（头部企业0.9，普通公司0.6） |
| 岗位分类不清晰 | 八大岗位分类体系 + 低端岗位过滤 |
| 新兴岗位检测太泛 | 基础技能白名单过滤（python+深度学习等组合不再标记为新兴） |

---

## 二、流水线架构

```
raw_jd.json (270条原始JD)
    │
    ├── [1] clean_jd.py ──── 清洗（9个子步骤）
    │     ├── 0. 字段名归一化（删除旧字段名，update_date→publish_date）
    │     ├── 1. JD文本清洗（去转义符/冗余前缀/残留冒号/末尾噪声）
    │     ├── 2. 岗位名称清洗（剥离待遇/条件噪声）
    │     ├── 2.5 公司名称清洗（去除截断标记"..."）
    │     ├── 3. AI岗位过滤（保留241条）
    │     ├── 4. 岗位相关性过滤（剔除12条低端非研发岗位）
    │     ├── 5. MinHash去重（排除近似重复）
    │     ├── 6. 置信度评分（公司名推断来源权重 + 时滞衰减）
    │     ├── 7. 同源通胀惩罚
    │     ├── 8. 技能堆砌检测
    │     └── 9. 置信度过滤 → cleaned_jd.json (17条)
    │
    ├── [2] extract_skills.py ── 抽取
    │     ├── jieba分词 + 技能词典匹配
    │     ├── 同义词归一化（如 torch→pytorch）
    │     ├── 技能置信度评分（幻觉防控）
    │     └── 八大岗位分类 → triples.json (77条三元组)
    │
    ├── [3] analyze_changes.py ── 分析
    │     ├── 新岗位发现（含基础技能白名单过滤）→ emerging_jobs.json
    │     └── 能力变化检测 → skill_changes.json
    │
    └── [4] export_graph.py ── 导出
          ├── 节点合并 + 边权重聚合
          ├── 八大分类着色
          └── 岗位技能清单生成 → graph_data.json
```

### 运行方式

```bash
# 将原始数据命名为 raw_jd.json 放在项目根目录，然后：
python run.py
```

---

## 三、输出文件详解

### 3.1 graph_data.json（核心文件，ECharts直接使用）

这是前端画图唯一必需的文件，包含力导向图的全部数据。

#### 顶层结构

```json
{
  "categories": [...],      // 9个分类定义
  "nodes": [...],           // 33个节点
  "links": [...],           // 66条边
  "jobSkills": {...},       // 岗位技能需求清单
  "categoryStats": {...},   // 八大分类统计
  "meta": {...}             // 元信息
}
```

#### categories（分类定义，9个）

| 索引 | name | description | 用途 |
|------|------|-------------|------|
| 0 | 底层研发 | AI基础设施与底层框架开发 | 岗位节点分类 |
| 1 | 算法模型 | 核心算法研究与模型训练 | 岗位节点分类 |
| 2 | AI工程落地 | AI模型工程化部署与落地应用 | 岗位节点分类 |
| 3 | 数据 | 数据采集、标注、处理与分析 | 岗位节点分类 |
| 4 | 硬件 | AI芯片与算力硬件 | 岗位节点分类 |
| 5 | 产品业务 | AI产品设计与业务落地 | 岗位节点分类 |
| 6 | 合规运营 | AI安全合规与质量保障 | 岗位节点分类 |
| 7 | 新兴轻门槛岗 | 新兴AI应用型低门槛岗位 | 岗位节点分类 |
| 8 | 技能 | AI技能 | 技能节点分类 |

**ECharts使用方式**：`categories[i]` 的索引与节点 `category` 字段一一对应，可直接传入 `option.series[0].categories`。

#### nodes（节点）

**岗位节点**（category 0-7）：

```json
{
  "id": "AI算法工程师",         // 唯一标识，用于边的 source/target
  "name": "AI算法工程师",       // 显示名称（已清洗，不含待遇噪声）
  "category": 1,               // 分类索引，对应 categories[1]="算法模型"
  "categoryName": "算法模型",   // 分类中文名（方便前端直接显示）
  "symbolSize": 80,            // 节点大小（按技能关联数缩放，30~80）
  "value": 28                  // 关联技能的总出现次数
}
```

**技能节点**（category 8）：

```json
{
  "id": "python",              // 技能名
  "name": "python",            // 显示名称
  "category": 8,               // 技能类
  "symbolSize": 41,            // 节点大小（按被需次数缩放，15~60）
  "value": 13,                 // 被多少个岗位需要
  "isEmerging": false          // 是否为白皮书认定的新兴技能
}
```

**ECharts使用方式**：
- `symbolSize` 可直接用作节点大小
- `category` 用于按分类着色
- `isEmerging=true` 的技能节点可用特殊样式（如高亮边框、星星图标）

#### links（边）

```json
{
  "source": "AI算法工程师",     // 岗位节点id
  "target": "python",          // 技能节点id
  "value": 4,                  // 共现次数（同一岗位下该技能出现的JD数）
  "confidence": 0.62,          // 平均置信度（0~1，幻觉防控评分）
  "lineStyle": {
    "width": 4,                // 线宽 = min(value, 5)
    "opacity": 0.82            // 透明度 = min(confidence+0.2, 1.0)
  }
}
```

**ECharts使用方式**：
- `value` 越大说明该技能对该岗位越核心，线的粗细可用 `lineStyle.width`
- `confidence` 越高说明该关联越可靠，透明度可用 `lineStyle.opacity`
- 建议低置信度（<0.5）的边用虚线样式

#### jobSkills（岗位技能需求清单）

每个岗位的技能列表，按频次降序排列，**用于"岗位需求能力分析"详情面板**。

```json
{
  "AI算法工程师": [
    {
      "skill": "python",          // 技能名
      "frequency": 4,             // 该岗位下出现次数
      "avgConfidence": 0.62,      // 平均置信度
      "isEmerging": false         // 是否新兴技能
    },
    {
      "skill": "强化学习",
      "frequency": 2,
      "avgConfidence": 0.72,
      "isEmerging": true          // ★ 新兴技能标记
    }
  ]
}
```

**前端用途**：
- 点击岗位节点 → 右侧面板展示该岗位的技能需求排行
- `frequency` → 柱状图/排行表
- `isEmerging=true` → 标注"新兴"标签
- `avgConfidence` → 显示可信度

#### categoryStats（八大分类统计）

```json
{
  "算法模型": {
    "jobCount": 8,              // 该分类下的岗位数
    "jobs": ["AI算法工程师", ...], // 岗位列表
    "skillCount": 22,           // 涉及的技能种数
    "description": "核心算法研究与模型训练"
  },
  "底层研发": {
    "jobCount": 0,              // 当前数据无此分类岗位
    "jobs": [],
    "skillCount": 0,
    "description": "AI基础设施与底层框架开发"
  }
}
```

**前端用途**：
- 分类概览饼图/柱状图
- `jobCount=0` 的分类可隐藏或灰显
- 点击分类 → 高亮该分类下所有岗位节点

#### meta（元信息）

```json
{
  "total_nodes": 33,
  "total_links": 66,
  "job_count": 10,
  "skill_count": 24
}
```

---

### 3.2 triples.json（岗位-技能三元组）

所有岗位与技能的关联明细，含置信度和分类。

```json
[
  {
    "job": "人工智能工程师",      // 清洗后的岗位名
    "category": "算法模型",       // 八大分类
    "skill": "agent",            // 技能名
    "source": "未知",             // 数据来源
    "confidence": 0.87,          // 技能置信度（幻觉防控）
    "company": "极达鑫"           // 发布公司
  }
]
```

**用途**：后台查询、表格展示、二次分析。当前共77条。

---

### 3.3 skill_changes.json（能力变化报告）

对比不同时间段，各岗位的技能需求变化。

```json
{
  "generated_at": "2026-07-04T23:36:24",
  "analyzed_jobs": 5,
  "changes": [
    {
      "job": "AI算法工程师",
      "additions": ["大模型", "java", "paddlepaddle", "go", ...],   // 新增技能
      "removals": ["tensorflow", "机器学习"],                       // 消失技能
      "unchanged": ["计算机视觉", "深度学习", "强化学习", ...],     // 保留技能
      "change_summary": "新增9项，移除2项"
    }
  ]
}
```

**前端用途**：
- "能力演变趋势"时间线图
- 新增/消失/保留的技能数量对比
- 点击岗位 → 展示其技能变化详情

---

### 3.4 emerging_jobs.json（新岗位候选）

基于技能组合异常检测发现的新兴岗位，**已过滤基础技能白名单**。

```json
{
  "generated_at": "2026-07-04T23:36:24",
  "total_candidates": 10,
  "industry_confirmed": 1,
  "candidates": [
    {
      "skill_pair": ["python", "强化学习"],
      "growth_rate": 2,
      "count": 2,
      "emergence_score": 0.91,
      "is_industry_confirmed": true,
      "status": "建议定义为新兴岗位",
      "sample_job_titles": ["机器视觉工程师", "AI软件工程师"],
      "reason": "符合行业白皮书认定方向；技能组合近期出现频率显著上升"
    }
  ]
}
```

**白名单过滤规则**：如果一个技能组合中两个技能都在基础技能白名单中（如 python+深度学习），则不纳入候选。只有至少包含一个新兴/前沿技能（如 transformer、大模型、强化学习）的组合才会被标记为新兴候选。

**前端用途**：
- "新岗位预警"卡片
- `is_industry_confirmed=true` → 白皮书确认，高优先级
- `emergence_score` → 按分数排序展示

---

### 3.5 cleaned_jd.json（清洗后的原始记录）

清洗后存活的完整JD记录，字段已归一化，旧字段名已删除。

```json
[
  {
    "job_title": "AI算法工程师",
    "company": "极达鑫",
    "job_description": "1、结合公司业务需求能独立开发业务Agent...",
    "source": "未知",
    "publish_date": "2026-06-30",
    "_confidence": 0.871,
    "_inflation_flag": false,
    "_skill_inflation_flag": false
  }
]
```

**字段说明**：
- `job_title`：已清洗，不含待遇/条件噪声
- `company`：已清洗，无截断标记
- `job_description`：已清洗，无转义符/冗余前缀
- `publish_date`：来自 update_date 映射（原始 publish_date 为0时自动用 update_date 填充）
- `_confidence`：综合置信度（0.625~0.958，有区分度）
- `_inflation_flag`：同源通胀嫌疑标记
- `_skill_inflation_flag`：技能堆砌嫌疑标记

当前共17条。

---

### 3.6 blocked_manual_review.json（阻断数据）

被系统拦截的低质量/通胀嫌疑数据，需人工确认。

```json
[
  {
    "job_title": "算法工程师助理",
    "company": "重庆宇树临风科技",
    "_confidence": 0.568
  }
]
```

**用途**：人工审核。判断是"误杀"（应恢复）还是"正确拦截"（保持阻断）。

---

### 3.7 filtered_low_end_jobs.json（低端岗位过滤数据）

被岗位相关性过滤器剔除的低端非研发岗位。

```json
[
  {
    "job_title": "数据标注/大模型标注工程师",
    "company": "重庆云谷创服人才科技"
  }
]
```

**用途**：人工确认是否有误杀（如某标注岗实际涉及模型训练研发）。

---

## 四、ECharts接入指南

### 4.1 力导向图（岗位-技能关系图谱）

```javascript
// 1. 加载数据
const data = await fetch('graph_data.json').then(r => r.json());

// 2. ECharts 配置
const option = {
  legend: {
    data: data.categories.map(c => c.name)
  },
  series: [{
    type: 'graph',
    layout: 'force',
    roam: true,
    categories: data.categories,
    data: data.nodes,
    links: data.links,
    force: {
      repulsion: 300,
      edgeLength: [100, 200]
    },
    label: {
      show: true,
      position: 'right'
    },
    emphasis: {
      focus: 'adjacency',
      lineStyle: { width: 4 }
    }
  }]
};
```

### 4.2 分类概览图（饼图/柱状图）

```javascript
// 使用 categoryStats 数据
const pieData = Object.entries(data.categoryStats)
  .filter(([_, v]) => v.jobCount > 0)  // 过滤空分类
  .map(([name, v]) => ({
    name: name,
    value: v.jobCount
  }));
```

### 4.3 岗位技能需求面板

```javascript
// 点击岗位节点时，展示 jobSkills 中的技能清单
node.on('click', (params) => {
  const jobName = params.data.id;
  const skills = data.jobSkills[jobName];
  // 渲染技能排行榜/雷达图
});
```

### 4.4 推荐配色方案

| 分类 | 推荐颜色 | 说明 |
|------|----------|------|
| 底层研发 | #5470C6 | 蓝色，象征基础设施 |
| 算法模型 | #91CC75 | 绿色，核心增长 |
| AI工程落地 | #FAC858 | 黄色，工程实践 |
| 数据 | #EE6666 | 红色，数据驱动 |
| 硬件 | #73C0DE | 浅蓝，硬件支撑 |
| 产品业务 | #3BA272 | 深绿，商业导向 |
| 合规运营 | #FC8452 | 橙色，安全警告 |
| 新兴轻门槛岗 | #9A60B4 | 紫色，新兴趋势 |
| 技能 | #5C7BD9 | 靛蓝，通用技能 |

---

## 五、数据质量指标

| 指标 | 当前值 | 说明 |
|------|--------|------|
| 原始数据量 | 270条 | raw_jd.json |
| AI岗位过滤 | 241/270 | 保留率 89.3% |
| 岗位相关性过滤 | 229/241 | 剔除12条低端非研发岗 |
| 去重后 | 20/229 | 去重率 91.3%（说明抄袭严重） |
| 最终通过 | 17/20 | 3条被置信度过滤阻断 |
| 技能种类 | 24种 | 词典匹配 |
| 三元组 | 77条 | 岗位-技能关联 |
| 图谱节点 | 33个 | 10岗位 + 24技能（含1个虚拟合并节点） |
| 图谱边 | 66条 | 岗位-技能关联 |
| 新兴技能 | 2个 | 强化学习、LoRA |
| 置信度范围 | 0.625~0.958 | 头部企业0.87+，普通公司0.80+ |

### 置信度分布

| 区间 | 数量 | 典型特征 |
|------|------|----------|
| ≥0.85 | 12条 | 头部企业 + 近期发布 |
| 0.75~0.85 | 3条 | 普通公司 + 近期发布 |
| 0.65~0.75 | 1条 | 普通公司 + 1-2月前发布 |
| <0.65 | 1条 | 半年前发布，时效衰减明显 |

---

## 六、文件依赖关系

```
graph_data.json ◄── ECharts前端直接读取
     ▲
     │ (由 export_graph.py 生成)
     │
triples.json ◄────── 后端查询/表格展示
     ▲
     │ (由 extract_skills.py 生成)
     │
cleaned_jd.json ◄─── 数据存档/审计
     ▲
     │ (由 clean_jd.py 生成)
     │
raw_jd.json ◄─────── 原始数据（用户提供）

skill_changes.json ◄─ 前端"能力变化趋势"图
emerging_jobs.json ◄── 前端"新岗位预警"卡片
blocked_manual_review.json ◄─ 人工审核专用
filtered_low_end_jobs.json ◄── 低端岗位过滤审计
```

---

## 七、脚本文件说明

| 文件 | 功能 | 输入 | 输出 |
|------|------|------|------|
| `skill_dict.py` | 技能词典 + 岗位分类 + 名称清洗 | 被调用 | — |
| `clean_jd.py` | 清洗：归一化+文本清洗+AI过滤+相关性过滤+去重+时滞+通胀+置信度 | raw_jd.json | cleaned_jd.json |
| `extract_skills.py` | 抽取：jieba分词+同义词归一化+三元组+幻觉防控 | cleaned_jd.json | triples.json |
| `analyze_changes.py` | 分析：新岗位(含白名单过滤)+能力变化 | cleaned_jd + triples | emerging_jobs + skill_changes |
| `export_graph.py` | 导出：ECharts图谱数据 | triples.json | graph_data.json |
| `run.py` | 一键运行全部流水线 | raw_jd.json | 全部输出文件 |

---

## 八、清洗机制详解

### 8.1 置信度评分（confidence_score）

综合评分 = 来源权威性(30%) + 字段完整度(40%) + 时效性(30%)

**来源权威性推断逻辑**：
- 有 source 字段 → 按平台权重（官网0.9，招聘网站0.7，猎聘0.6）
- 无 source 字段 → 根据公司名推断：
  - 命中头部企业名单（华为/阿里/腾讯/百度/长安/科大讯飞等）→ 0.9
  - 其他公司 → 0.6

**时效性计算**：
- publish_date 来自 update_date 自动映射（原始 publish_date 为0时用 update_date 填充）
- 近期JD时效权重≈1.0，半年前≈0.85，1年前≈0.05

### 8.2 岗位相关性过滤（filter_ai_relevance）

**低端岗位关键词黑名单**：数据标注、标注员、AI训练师（非研发）、AI绘图员、AI客服等

**核心研发词保护**：即使标题含低端词，但描述中有"算法""工程师""研发""深度学习"等核心词，仍保留。

**双重检查**：同时检查原始标题和清洗后的标题，避免"数据标注/工程师"清洗后只剩"数据标注"漏过。

### 8.3 基础技能白名单（BASIC_SKILL_WHITELIST）

新兴岗位检测时，如果技能组合中两个技能都在白名单中，则跳过不纳入候选。

**白名单内容**：
- 编程语言：python, c++, java, go, sql
- 通用框架：pytorch, tensorflow, keras, scikit-learn, pandas, numpy
- 通用AI概念：机器学习, 深度学习, 计算机视觉, 自然语言处理, 数据分析
- 通用工程：linux, docker, git, mysql, redis

**效果**：python+深度学习、pytorch+机器学习等基础组合不再被标记为"新兴"，只有含 transformer、大模型、强化学习等前沿技能的组合才会被纳入候选。

---

## 九、常见问题

### Q1: 为什么某些分类（底层研发/数据/硬件等）的 jobCount 为 0？
当前数据集以算法模型岗为主，暂无底层研发、数据工程、硬件等类型的岗位。扩大数据源后这些分类会有内容。前端可隐藏 `jobCount=0` 的分类。

### Q2: confidence 低于多少的边不可信？
- `≥ 0.7`：可信（白皮书认证或多源交叉验证通过）
- `0.5~0.7`：一般（仅词典匹配，无交叉验证）
- `< 0.5`：低信（已在清洗阶段被阻断，不会出现在最终数据中）

### Q3: 如何更新数据？
替换 `raw_jd.json`，重新运行 `python run.py` 即可。所有输出文件会自动覆盖。

### Q4: 岗位名称中的"朝九晚六""五险一金"等噪声如何处理？
在 `clean_jd.py` 的 `clean_titles()` 步骤中调用 `clean_job_title()` 自动剥离待遇/条件噪声词、平台名前缀、括号标注、薪资数字等。

### Q5: isEmerging 标记的依据是什么？
对照 `INDUSTRY_STANDARD_TERMS`（国家职业分类大典2025增补 + 信通院AI白皮书 + Gartner成熟度曲线）进行匹配。命中的技能标记为新兴。

### Q6: 为什么有些JD的 publish_date 来自 update_date？
原始数据中 publish_date 字段全为0（无效值），而实际发布时间存储在 update_date 字段中。`normalize_fields()` 会自动将 update_date 映射为 publish_date，确保时滞衰减功能正常生效。

### Q7: 哪些公司会被识别为"头部企业"？
包括：科大讯飞、华为、阿里、腾讯、字节、百度、长安、小米、京东、美团、滴滴、网易、商汤、旷视、依图、云从、寒武纪、地平线、大疆、中兴、联想，以及公司名含"中科""清华""北大"的机构。
