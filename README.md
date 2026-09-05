# 🧠 Elite Agent Skills — مستودع مهارات الوكلاء الاحترافي

> A curated, production-grade library of **Agent Skills** (`SKILL.md`) that turn a generic AI coding
> agent into a disciplined senior engineer, designer, DBA, technical writer and release manager.
>
> مكتبة منتقاة من **مهارات الوكلاء** بصيغة `SKILL.md` تحوّل أي وكيل ذكاء اصطناعي عام إلى
> مهندس أول منضبط، ومصمم، ومهندس قواعد بيانات، وكاتب تقني، ومدير إصدارات.

---

## 1. لماذا هذا المستودع؟ / Why this repo

النماذج اللغوية ليست غبية — لكنها **بلا سياق**. بدون قواعد صريحة سيختار الوكيل أول حل يعرفه،
لا أفضل حل. هذا المستودع يشفّر المعرفة الضمنية للخبراء البشريين (قوانين التصميم، معايير الأمان،
سياسات المتاجر، أنماط المعمارية) في مهارات قابلة للتحميل التلقائي.

Three principles / ثلاثة مبادئ:

| # | Principle | القاعدة |
|---|-----------|---------|
| 1 | **Rules over vibes** — every instruction is falsifiable and checkable | كل تعليمة قابلة للتحقق |
| 2 | **Progressive disclosure** — `SKILL.md` stays < 500 lines; depth lives in `references/` | الإيجاز في الواجهة والعمق في المراجع |
| 3 | **Executable truth** — a CI workflow proves the agent's output actually builds | الـ CI هو الحكم النهائي |

---

## 2. البنية / Repository layout

```
.
├── skills/                     # كل المهارات (Agent Skills)
│   ├── android/                #   مسار الأندرويد (المسار العميق الأول)
│   ├── design/                 #   UI / UX / Icons / Logos
│   ├── data/                   #   قواعد البيانات والنمذجة
│   ├── delivery/               #   CI/CD والنشر والمتاجر
│   └── docs/                   #   التوثيق والكتابة التقنية
├── docs/
│   ├── ROADMAP.md              # الخطة الكاملة وكل المهارات المخططة
│   ├── SKILL_AUTHORING_GUIDE.md# كيف تُكتب مهارة نخبوية
│   ├── AGENT_OPERATING_MODEL.md# كيف يستهلك الوكيل هذه المهارات
│   └── SKILL_TEMPLATE.md       # القالب الرسمي
├── tools/validate_skills.py    # مدقق البنية والـ frontmatter
└── templates/github-workflows/ # قوالب CI: تدقيق المهارات + بناء أندرويد + إصدار
```

## 3. تشغيل سريع / Quick start

```bash
# 1. اربط المهارات بوكيلك (Claude Code)
ln -s "$PWD/skills" ~/.claude/skills/elite         # أو انسخ المجلد داخل مشروعك: .claude/skills/
# Codex: .agents/skills/     |  OpenClaw: ~/.openclaw/skills/

# 2. تحقّق من صحة كل المهارات
python3 tools/validate_skills.py

# 3. اطلب من الوكيل
#    "Bootstrap a Kotlin Compose app called Tasky, then wire the CI"
```

### كيف يختار الوكيل المهارة؟
حقل `description` في الـ frontmatter هو **إشارة التوجيه** الوحيدة. يُحمَّل عند بدء الجلسة فقط
الاسم والوصف؛ بقية الملف يُقرأ عند الحاجة. لذلك كل وصف يحتوي: *ماذا تفعل المهارة* + *متى تُستدعى* + كلمات مفتاحية.

## 4. المهارات المتوفرة الآن / Available skills

| Skill | المجال | الغرض |
|---|---|---|
| `android-project-bootstrap` | Android | إنشاء مشروع Gradle حديث (AGP 9، version catalog، convention plugins) |
| `android-kotlin-architecture` | Android | Clean Architecture + MVVM/MVI، Hilt، Coroutines/Flow |
| `android-java-legacy` | Android | صيانة وتحديث أكواد Java القديمة والهجرة إلى Kotlin |
| `android-compose-ui` | Android | Jetpack Compose: state hoisting، أداء، Material 3 |
| `android-room-database` | Data | تصميم Room/SQLite، الهجرات، الاختبار |
| `android-testing-quality` | Android | هرم الاختبار، JUnit5، Turbine، Compose tests، Paparazzi |
| `android-performance` | Android | Baseline Profiles، startup، jank، R8، حجم APK |
| `android-security-hardening` | Android | OWASP MASVS، تخزين آمن، شبكات، تشويش، أسرار CI |
| `android-cicd-github-actions` | Delivery | مصفوفة بناء، توقيع، cache، رفع للمسارات |
| `android-play-release` | Delivery | متطلبات Play 2026 (API 36)، مسارات الطرح، توقيع التطبيق |
| `ui-design-system` | Design | التوكنز، الشبكة، السلم النمطي، اللون، الحركة |
| `ux-flow-architect` | Design | خرائط الرحلات، قوانين UX، حالات الفراغ والخطأ |
| `app-icon-designer` | Design | أيقونات تكيفية/ثيمية + كل المقاسات المطلوبة |
| `logo-brand-designer` | Design | الهوية البصرية، الشعار، دليل الاستخدام |
| `technical-docs-writer` | Docs | Diátaxis، README، ADR، سجل التغييرات، صفحة المتجر |

> الخطة الكاملة (٦٠+ مهارة قادمة: Flutter، Web/TS، Backend، iOS، KMP، AI/RAG…) في
> [`docs/ROADMAP.md`](docs/ROADMAP.md).

## 5. المساهمة / Contributing
اقرأ [`docs/SKILL_AUTHORING_GUIDE.md`](docs/SKILL_AUTHORING_GUIDE.md) ثم انسخ
[`docs/SKILL_TEMPLATE.md`](docs/SKILL_TEMPLATE.md). كل PR يمرّ على `validate_skills.py`.

## 6. الرخصة
MIT.
