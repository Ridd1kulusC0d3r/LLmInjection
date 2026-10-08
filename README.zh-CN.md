<p align="center">
  <img src="assets/llminjection-banner.svg" alt="LLMInjection：LLM 与智能体系统威胁态势" width="100%">
</p>

<!-- lang-bar -->
[English](README.md) · [Português](README.pt-BR.md) · [Español](README.es.md) · **简体中文** · [Русский](README.ru.md)
<!-- /lang-bar -->

> 本译文为机器辅助翻译，尚未经母语者审校。以英文版为准。如需勘误，请参阅 [docs/TRANSLATIONS.md](docs/TRANSLATIONS.md)。

面向 AI、大语言模型（LLM）与智能体系统的开放威胁情报：攻击者、攻击活动、攻击技术、安全测试用例、检测和控制措施，并与支撑每条结论的证据相互关联。

**[Explorer](https://ridd1kulusc0d3r.github.io/LLmInjection/#lang=zh)** · [文档](docs/README.md) · [方法论](docs/METHODOLOGY.md)

---

## 数据概览

<!-- gen:stats-zh:start -->
| 攻击者 | 攻击活动 | 事件 | 漏洞 | 技术 | 来源 |
|:---:|:---:|:---:|:---:|:---:|:---:|
| **8** | **10** | **30** | **9** | **28** | **54** |

| 测试用例 | 检测 | 控制措施 | 框架 | 模型系列 | 关联关系 | 生态系统项目 |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **40** | **45** | **32** | **19** | **12** | **215** | **106** |
<!-- gen:stats-zh:end -->

LLMInjection **不是提示词合集**。每条重要结论都标注来源等级、置信度、核实日期、框架对应关系以及防御视角。

## 内容构成

| 层 | 包含内容 | 入口 |
|---|---|---|
| **攻击者与攻击活动** | 使用 AI 的国家背景和犯罪组织，保留厂商发布的原始跟踪标签 | [`data/actors.json`](data/actors.json) |
| **拉丁美洲** | AI 在该地区被用于攻击的情况，区分报告所称与未称的内容 | [西班牙语概述](docs/es/PANORAMA-LATAM.md)（另有[葡萄牙语版](docs/pt-BR/PANORAMA-BRASIL-LATAM.md)） |
| **威胁态势** | 2026 年的引用指标、领域与研究线索 | [Landscape 2026](docs/THREAT-LANDSCAPE-2026.md) |
| **技术与框架** | 带成熟度等级的技术，映射到 ATLAS、OWASP、NIST、SAIF 和 MAESTRO | [框架](docs/FRAMEWORKS.md) |
| **安全实验环境** | 面向提示词、RAG、智能体、MCP 和供应链的防御性测试用例 | [测试用例](docs/TEST-CASES.md) |
| **检测** | 检测假设与 Sigma 起步规则 | [检测工程](docs/DETECTION-ENGINEERING.md) |
| **生态系统** | 相关项目，按其所能支撑的结论分类 | [生态系统图](docs/ECOSYSTEM.md) |

## 原则

1. **已观察到的事件、研究中验证的技术和实验室示例不相混淆。** 越狱提示词合集可以启发测试，但永远无法证明某个攻击者使用过该技术。
2. **推断不等于证实。** 当 AI 的使用是根据痕迹推断出来时，记录会明确说明。
3. **没有证据就不合并厂商标签**，不将其合并为通用别名。
4. **成熟度来自图谱。** 每项技术被归类为“已在实际攻击中观察到”“已披露漏洞”“研究中已验证”或“暂无关联证据”，校验机制会阻止该字段偏离数据。

## 快速开始

```bash
make check         # 代码检查、测试、数据校验和图谱审计
make build         # 图谱、STIX、静态 API、Navigator 图层和图表
python scripts/query_intel.py search "prompt injection"
python scripts/osint_ioc.py report.md --enrich    # 提取 IOC；用 CISA KEV 和 EPSS 补充 CVE 信息
```

Python 3.12，仅使用标准库。

## 参与贡献

有价值的贡献是补充**证据、关联关系、测试、检测或勘误**，而不是夸大其词。请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)，优先使用一手来源，保留不确定性，并在提交 pull request 之前运行 `make check`。

## 许可证

Apache-2.0。见 [LICENSE](LICENSE)。
