# GitHub Actions templates — قوالب سير العمل

> هذه ملفات جاهزة للنسخ. لم تُوضع مباشرة في `.github/workflows/` لأن تطبيق GitHub المستخدم في
> هذه الجلسة لا يملك صلاحية `workflows`. انسخها يدويًا (أو عبر الأوامر أدناه) لتفعيلها.

| الملف | الوجهة | الغرض |
|---|---|---|
| `validate-skills.yml` | **هذا المستودع** → `.github/workflows/` | تدقيق كل `SKILL.md` + فحص Markdown والروابط |
| `android-build.yml` | مستودع تطبيق أندرويد | بوابة PR: detekt/lint/اختبارات/بناء + مصفوفة محاكي |
| `android-release.yml` | مستودع تطبيق أندرويد | بناء AAB موقّع عند وسم `v*` + نشر محمي على Play |

## تفعيل مدقق المهارات في هذا المستودع
```bash
mkdir -p .github/workflows
cp templates/github-workflows/validate-skills.yml .github/workflows/
git add .github/workflows/validate-skills.yml
git commit -m "ci: validate skills on every push"
git push
```

## استخدامها في مشروع أندرويد
```bash
mkdir -p .github/workflows
cp templates/github-workflows/android-build.yml   .github/workflows/
cp templates/github-workflows/android-release.yml .github/workflows/
```
ثم عدّل: `packageName`، أسماء المهام في Gradle، ومستويات API في المصفوفة.

### الأسرار المطلوبة للإصدار
| Secret | القيمة |
|---|---|
| `KEYSTORE_BASE64` | `base64 -w0 upload-keystore.jks` |
| `KEYSTORE_PASSWORD` / `KEY_ALIAS` / `KEY_PASSWORD` | بيانات التوقيع |
| `PLAY_SERVICE_ACCOUNT_JSON` | حساب خدمة بصلاحية Release manager على هذا التطبيق فقط |

وأنشئ بيئة محمية باسم `production` مع مراجعين مطلوبين قبل تفعيل وظيفة النشر.

> التفاصيل الكاملة والشروحات في المهارة `skills/delivery/android-cicd-github-actions/`.
