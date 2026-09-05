# ✍️ Skill Authoring Guide — دليل تأليف مهارة نخبوية

## 1. بنية المجلد

```
skills/<domain>/<skill-name>/
├── SKILL.md            # إلزامي — الواجهة المختصرة (< 500 سطر)
├── references/         # اختياري — العمق: جداول، قوانين، أمثلة طويلة
├── assets/             # اختياري — قوالب ملفات جاهزة للنسخ
└── scripts/            # اختياري — سكربتات تنفّذ دون قراءة محتواها
```

> **Progressive disclosure:** يُحمَّل `name` + `description` فقط في سياق الوكيل عند الإقلاع.
> `SKILL.md` يُقرأ عند التفعيل. `references/*` تُقرأ فقط عند الحاجة — لذلك ضع فيها كل ما هو طويل.
> اجعل الإشارات المرجعية **بعمق مستوى واحد** فقط (`references/x.md` لا `references/a/b/c.md`).

## 2. الـ Frontmatter المعياري

```yaml
---
name: android-compose-ui              # = اسم المجلد، kebab-case، ≤ 64 حرفًا
description: >-                       # ≤ 1024 حرفًا — ماذا + متى + كلمات مفتاحية
  Builds and reviews Jetpack Compose UI ... Use when the user mentions Compose,
  @Composable, Material 3, recomposition, or Android screen implementation.
version: 1.0.0
license: MIT
category: android
tags: [android, kotlin, compose, ui, material3]
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob, WebFetch]
metadata:
  maturity: stable                    # draft | beta | stable
  arabic_summary: "بناء ومراجعة واجهات Jetpack Compose ..."
---
```

الحقلان `name` و`description` فقط إلزاميان في المواصفة المفتوحة؛ البقية تحسّن الاكتشاف
والتوافق مع Claude Code / Codex / OpenClaw.

### قواعد كتابة الـ description (الأهم على الإطلاق)
- ابدأ بفعل: `Builds…`, `Audits…`, `Designs…`.
- اذكر **متى**: `Use when the user mentions X, Y, or Z.`
- ضمّن المرادفات التي سيكتبها المستخدم فعلًا (`gradle`, `apk`, `aab`, `play store`).
- لا تكتب `Helps with Android stuff` — لا إشارة توجيه فيها.

## 3. هيكل جسم المهارة (ثابت في كل المستودع)

```markdown
# <Title>            ← سطر واحد يشرح الدور
## When to use / When NOT to use
## Non-negotiables   ← MUST / NEVER — قابلة للتحقق
## Version pins      ← الإصدارات المثبتة (المكان الوحيد للمعلومات الزمنية)
## Workflow          ← خطوات مرقّمة يتبعها الوكيل حرفيًا
## Patterns          ← مقتطفات كود صحيحة ✅ مقابل خاطئة ❌
## Anti-patterns
## Definition of Done ← قائمة تحقق [ ]
## References        ← روابط `references/*.md` ومصادر رسمية
## ملخص عربي         ← 5–10 أسطر
```

## 4. قواعد الأسلوب
| ✅ افعل | ❌ لا تفعل |
|---|---|
| صيغة الأمر: "Do X" | "You might consider…" |
| أمثلة ملموسة بأسماء ملفات حقيقية | أمثلة مجردة `foo/bar` |
| مصطلح واحد ثابت لكل مفهوم | ترادف عشوائي (`screen`/`page`/`view`) |
| أرقام حدّية (`< 16ms`, `≥ 80% coverage`) | "سريع"، "جيد" |
| تثبيت الإصدارات في قسم واحد | نثر الأرقام في كل الملف |

## 5. الاختبار قبل الدمج
```bash
python3 tools/validate_skills.py            # بنية + frontmatter + حدود
python3 tools/validate_skills.py --strict   # يفشل أيضًا على التحذيرات
```
اختبر عمليًا: افتح جلسة وكيل نظيفة، اطلب المهمة بلغة المستخدم الطبيعية، وتأكد أن المهارة
تُفعَّل تلقائيًا من الوصف وحده.
