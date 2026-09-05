# Contributing — المساهمة

## قبل أن تبدأ
1. اقرأ [`docs/SKILL_AUTHORING_GUIDE.md`](docs/SKILL_AUTHORING_GUIDE.md).
2. تحقّق من [`docs/ROADMAP.md`](docs/ROADMAP.md) — قد تكون المهارة مخططة بالفعل.

## إضافة مهارة جديدة

```bash
mkdir -p skills/<domain>/<skill-name>/references
cp docs/SKILL_TEMPLATE.md skills/<domain>/<skill-name>/SKILL.md
# املأ الملف، ثم:
python3 tools/validate_skills.py
```

القواعد الصارمة:
- `name` في الـ frontmatter = اسم المجلد بالضبط، kebab-case.
- `description` يحوي جملة `Use when ...` مع كلمات مفتاحية حقيقية سيكتبها المستخدم.
- جسم `SKILL.md` أقل من 500 سطر — كل ما هو أطول يذهب إلى `references/`.
- أقسام إلزامية: `## When to use`, `## Non-negotiables`, `## Definition of Done`.
- أقسام موصى بها: `## Workflow`, `## References`, `## ملخص عربي`.
- كل قاعدة قابلة للتحقق: أرقام وحدود، لا "جيد" و"سريع".
- الإصدارات المثبتة في قسم `## Version pins` فقط.

## الفروع والـ commits
- فروع: `feat/<slug>`, `fix/<slug>`, `docs/<slug>`.
- Conventional Commits: `feat(android): add compose testing skill`.

## قبل فتح PR
- [ ] `python3 tools/validate_skills.py` يمرّ بلا أخطاء.
- [ ] لا روابط مكسورة، لا معلومات إصدارات خارج `Version pins`.
- [ ] أضفت المهارة إلى جدول README و`docs/ROADMAP.md`.
- [ ] اختبرت المهارة عمليًا مع وكيل حقيقي: هل تُفعَّل تلقائيًا من الوصف؟

## معايير الجودة (سنرفض PR لا يحققها)
| المعيار | الحد |
|---|---|
| مصادر رسمية | كل قاعدة مبنية على وثيقة رسمية أو ممارسة مثبتة |
| أمثلة كود | ✅ صحيح و❌ خاطئ، حقيقية لا مجردة |
| Anti-patterns | ≥ 5 أخطاء شائعة موثقة |
| Definition of Done | قائمة تحقق قابلة للقياس |
| ملخص عربي | موجود ودقيق |
