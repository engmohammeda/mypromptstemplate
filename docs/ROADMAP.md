# 🗺️ ROADMAP — خطة بناء مكتبة المهارات

الهدف: مستودع واحد يوجّه الوكلاء لإنتاج برمجيات بمستوى فريق نخبة، لكل منصة، من الفكرة إلى المتجر.

## المنهجية (تُطبَّق على كل مهارة)

1. **Research** — مصادر رسمية فقط (Android Developers، Material 3، Play Console، OWASP MASVS، NN/g، WCAG).
2. **Distill** — تحويل المعرفة إلى قواعد قابلة للتحقق (`MUST` / `SHOULD` / `NEVER`).
3. **Templatize** — مقتطفات كود جاهزة لكل منصة (لا شرح نظري بلا كود).
4. **Gate** — قائمة تحقق نهائية + workflow يثبت النتيجة.
5. **Iterate** — كل مهارة لها `version` وسجل تغيير.

## المراحل

### المرحلة 0 — الأساس ✅
- [x] معيار البنية (`SKILL.md` + `references/` + `assets/` + `scripts/`)
- [x] دليل التأليف + القالب الرسمي
- [x] مدقق آلي `tools/validate_skills.py` + workflow
- [x] نموذج تشغيل الوكيل (Agent Operating Model)

### المرحلة 1 — مسار الأندرويد العميق ✅ (هذه الجولة)
`skills/android/*`, `skills/data/android-room-database`, `skills/delivery/*`

| المهارة | الحالة |
|---|---|
| android-project-bootstrap | ✅ |
| android-kotlin-architecture | ✅ |
| android-java-legacy | ✅ |
| android-compose-ui | ✅ |
| android-room-database | ✅ |
| android-testing-quality | ✅ |
| android-performance | ✅ |
| android-security-hardening | ✅ |
| android-cicd-github-actions | ✅ |
| android-play-release | ✅ |
| ui-design-system | ✅ |
| ux-flow-architect | ✅ |
| app-icon-designer | ✅ |
| logo-brand-designer | ✅ |
| technical-docs-writer | ✅ |

### المرحلة 2 — التصميم المتقدم والوسائط
- `motion-design-spec` — منحنيات، مدد، مبادئ الحركة لكل منصة
- `accessibility-auditor` — WCAG 2.2 AA + TalkBack + أهداف اللمس
- `localization-rtl` — العربية/RTL، التعددية، pseudo-localization
- `illustration-empty-states`, `design-token-pipeline` (Style Dictionary)
- `screenshot-store-assets` — لقطات المتجر الآلية (Fastlane screengrab)

### المرحلة 3 — منصات إضافية
- Flutter: `flutter-architecture`, `flutter-widget-ui`, `flutter-cicd`
- Web: `react-nextjs-architecture`, `typescript-strict-standards`, `tailwind-design-system`, `web-perf-core-web-vitals`
- Backend: `api-design-openapi`, `nodejs-service`, `spring-boot-service`, `postgres-schema-design`, `redis-caching`
- iOS/KMP: `swiftui-ui`, `ios-appstore-release`, `kmp-shared-module`
- Desktop: `electron-tauri-packaging`, `msix-microsoft-store`

### المرحلة 4 — البيانات والذكاء
- `database-modeling-normalization`, `migration-strategy`, `sql-performance-tuning`
- `analytics-events-taxonomy`, `ab-testing`
- `rag-pipeline-design`, `llm-prompt-engineering`, `eval-harness`

### المرحلة 5 — الحوكمة والتشغيل
- `git-workflow-conventional-commits`, `code-review-checklist`
- `observability-logging-metrics`, `incident-runbook`
- `threat-modeling-stride`, `privacy-gdpr-datasafety`
- `agent-orchestration` — تسليم المهام بين الوكلاء (مصمم → مهندس → مراجع → ناشر)

## معايير القبول لأي مهارة قبل الدمج
- [ ] `name` مطابق لاسم المجلد، kebab-case.
- [ ] `description` يذكر *ماذا* و*متى* + كلمات مفتاحية (≤ 1024 حرفًا).
- [ ] جسم الملف < 500 سطر، والعمق في `references/`.
- [ ] قسم **Non-negotiables** بصيغة MUST/NEVER.
- [ ] قسم **Definition of Done** كقائمة تحقق.
- [ ] مقتطفات كود حقيقية وقابلة للنسخ.
- [ ] لا معلومات حساسة زمنيًا خارج قسم *Version pins*.
- [ ] يمرّ `python3 tools/validate_skills.py`.
