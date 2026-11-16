# Portfolio case study

`index.html` 是 Talent Radar 的单文件作品集页面，可直接双击打开，也可放到任意静态站点。

## 更新时机
- 发布新 Release：修改 `<a href="...releases/tag/...">` 的文字和链接。
- 测试数量变化：同步修改“工程要点”里的 CI 数字。
- 真人验证或数据池拿到真实数据：先改 `research/STATUS.md`，再改本页面的“证据边界”，保留样本数与运行命令。
- 收款链接配置完成：销售页与 zip 由 `tools/set_payment_url.py` 更新；作品集页面不直接放收款链接。

## 口径
- 定位为商业小工具副线，不写成主研究项目。
- 静态 Demo 没有后端；AI 深挖和数据池要本地 `serve.py`。
- 不做心理测评认证、心理诊断、信度效度已验证等表述。
