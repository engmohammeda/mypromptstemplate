# 🤖 Agent Operating Model — نموذج تشغيل الوكلاء

كيف تتحول هذه المهارات إلى خط إنتاج فعلي: **وكيل واحد لكل دور، مصنع واحد للتسليم.**

## 1. الأدوار (Role → Skills)

| الدور | المهارات التي يحمّلها | المخرجات |
|---|---|---|
| 🧭 Product/UX | `ux-flow-architect`, `technical-docs-writer` | PRD، خرائط الرحلات، معايير القبول |
| 🎨 Designer | `ui-design-system`, `app-icon-designer`, `logo-brand-designer` | توكنز، مواصفة شاشات، أصول |
| 🏗️ Architect | `android-kotlin-architecture`, `android-room-database` | ADRs، تقسيم الموديولات، المخطط |
| 👨‍💻 Implementer | `android-project-bootstrap`, `android-compose-ui`, `android-java-legacy` | كود يُبنى |
| 🔬 QA | `android-testing-quality`, `android-performance` | اختبارات، ميزانيات أداء |
| 🔐 Security | `android-security-hardening` | تقرير MASVS، إصلاحات |
| 🚀 Release | `android-cicd-github-actions`, `android-play-release` | AAB موقّع، طرح تدريجي |

## 2. دورة التسليم

```
Idea → [UX] PRD+Flows → [Design] Tokens+Screens → [Architect] ADR+Modules
     → [Implementer] Code on feature branch → push
     → GitHub Actions: lint · detekt · unit · instrumented · assemble
     → [QA/Security] gates → [Release] tag → signed AAB → Play internal track
```

**القاعدة الذهبية:** الوكيل لا يعلن النجاح بناءً على قراءته للكود، بل على **خضرة الـ CI**.

## 3. عقد التسليم بين الوكلاء (Handoff Contract)
كل دور يُنهي عمله بملف `handoff/<role>.md`:

```markdown
## Delivered      # ما أُنجز فعليًا (ملفات + مسارات)
## Decisions      # قرارات + بدائل مرفوضة + السبب
## Open questions # ما يحتاج قرار بشري
## Next role      # ماذا يفعل الدور التالي بالضبط
## Verification   # الأمر الذي يثبت العمل (رابط CI run)
```

## 4. قواعد سلوكية عامة لأي وكيل في هذا المستودع
- **MUST** يقرأ المهارة المطابقة قبل كتابة أي سطر كود.
- **MUST** يشغّل البناء/الاختبار محليًا أو عبر CI قبل ادعاء الإنجاز.
- **MUST** يفصل التغييرات على فروع `feat/*`, `fix/*` مع Conventional Commits.
- **NEVER** يكتب أسرارًا (keystore، API keys) في المستودع — GitHub Secrets فقط.
- **NEVER** يرفع إصدارًا رئيسيًا لمكتبة دون قراءة سجل التغييرات.
- عند التعارض بين رأي النموذج والمهارة → **المهارة هي المرجع**.

## 5. تركيب المهارات (Skill Composition)
مهمة "شاشة تسجيل دخول جديدة" تُفعّل بالترتيب:
`ux-flow-architect` → `ui-design-system` → `android-compose-ui` → `android-kotlin-architecture`
→ `android-testing-quality` → `android-security-hardening` → `android-cicd-github-actions`.

## ملخص عربي
هذا الملف يحوّل المهارات المتفرقة إلى منظومة: من يفعل ماذا، وبأي ترتيب، وما الدليل على الإنجاز.
