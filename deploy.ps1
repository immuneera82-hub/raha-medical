# 🚀 سكريبت النشر التلقائي لـ Raha Medical
# Automatic Deployment Script
# PowerShell Script

# الألوان للرسائل
$ErrorColor = "Red"
$SuccessColor = "Green"
$InfoColor = "Cyan"
$WarningColor = "Yellow"

Write-Host "================================================" -ForegroundColor $InfoColor
Write-Host "   🚀 Raha Medical - سكريبت النشر التلقائي   " -ForegroundColor $InfoColor
Write-Host "================================================" -ForegroundColor $InfoColor
Write-Host ""

# الخطوة 1: التحقق من أننا في المجلد الصحيح
Write-Host "📁 الخطوة 1: التحقق من المجلد..." -ForegroundColor $InfoColor
$currentPath = Get-Location
if ($currentPath.Path -notlike "*\RM") {
    Write-Host "❌ خطأ: يجب تشغيل السكريبت من مجلد RM" -ForegroundColor $ErrorColor
    Write-Host "المجلد الحالي: $currentPath" -ForegroundColor $ErrorColor
    exit 1
}
Write-Host "✅ المجلد صحيح: $currentPath" -ForegroundColor $SuccessColor
Write-Host ""

# الخطوة 2: التحقق من وجود Git
Write-Host "🔍 الخطوة 2: التحقق من Git..." -ForegroundColor $InfoColor
try {
    $gitVersion = git --version
    Write-Host "✅ Git موجود: $gitVersion" -ForegroundColor $SuccessColor
} catch {
    Write-Host "❌ خطأ: Git غير مثبت" -ForegroundColor $ErrorColor
    exit 1
}
Write-Host ""

# الخطوة 3: التحقق من الملفات السرية
Write-Host "🔐 الخطوة 3: التحقق من الملفات السرية..." -ForegroundColor $InfoColor
$secretFiles = git ls-files | Select-String -Pattern "\.env$|credentials|\.key$|\.pem$"
if ($secretFiles) {
    Write-Host "⚠️  تحذير: وجدت ملفات سرية في Git:" -ForegroundColor $WarningColor
    $secretFiles | ForEach-Object { Write-Host "   - $_" -ForegroundColor $WarningColor }
    
    $response = Read-Host "هل تريد إزالتها من Git؟ (y/n)"
    if ($response -eq "y" -or $response -eq "Y") {
        foreach ($file in $secretFiles) {
            Write-Host "   إزالة $file..." -ForegroundColor $InfoColor
            git rm --cached $file
        }
        Write-Host "✅ تم إزالة الملفات السرية" -ForegroundColor $SuccessColor
    }
} else {
    Write-Host "✅ لا توجد ملفات سرية في Git" -ForegroundColor $SuccessColor
}
Write-Host ""

# الخطوة 4: عرض التغييرات
Write-Host "📝 الخطوة 4: مراجعة التغييرات..." -ForegroundColor $InfoColor
git status --short
Write-Host ""

# الخطوة 5: إضافة الملفات
Write-Host "➕ الخطوة 5: إضافة الملفات..." -ForegroundColor $InfoColor
$response = Read-Host "هل تريد إضافة جميع التغييرات؟ (y/n)"
if ($response -eq "y" -or $response -eq "Y") {
    git add .
    Write-Host "✅ تم إضافة جميع الملفات" -ForegroundColor $SuccessColor
} else {
    Write-Host "ℹ️  يرجى إضافة الملفات يدوياً" -ForegroundColor $InfoColor
    exit 0
}
Write-Host ""

# الخطوة 6: Commit
Write-Host "💾 الخطوة 6: حفظ التغييرات..." -ForegroundColor $InfoColor
$commitMessage = @"
✨ تحديثات الشفافية والامتثال القانوني

- حذف سياسة الإلغاء والاسترداد من الشروط والأحكام
- تعديل القانون المعمول به ليقتصر على قوانين الهند فقط
- إعادة صياغة إجابة التكاليف في FAQ لتوضيح أنها تقديرية
- توضيح ما تشمله التكاليف وما لا تشمله
- تحسين ملف .gitignore للحماية الأفضل
- إضافة ملفات التوثيق والأمان الشاملة
"@

Write-Host "رسالة الـ Commit:" -ForegroundColor $InfoColor
Write-Host $commitMessage -ForegroundColor $InfoColor
Write-Host ""

$response = Read-Host "هل تريد المتابعة؟ (y/n)"
if ($response -eq "y" -or $response -eq "Y") {
    git commit -m $commitMessage
    Write-Host "✅ تم حفظ التغييرات" -ForegroundColor $SuccessColor
} else {
    Write-Host "❌ تم إلغاء العملية" -ForegroundColor $WarningColor
    exit 0
}
Write-Host ""

# الخطوة 7: Push إلى GitHub
Write-Host "🌐 الخطوة 7: رفع على GitHub..." -ForegroundColor $InfoColor
$response = Read-Host "هل تريد رفع التحديثات على GitHub؟ (y/n)"
if ($response -eq "y" -or $response -eq "Y") {
    try {
        git push origin main
        Write-Host "✅ تم رفع التحديثات بنجاح" -ForegroundColor $SuccessColor
    } catch {
        Write-Host "⚠️  قد تحتاج إلى Pull أولاً" -ForegroundColor $WarningColor
        $response = Read-Host "هل تريد Pull ثم Push؟ (y/n)"
        if ($response -eq "y" -or $response -eq "Y") {
            git pull origin main --rebase
            git push origin main
            Write-Host "✅ تم رفع التحديثات بنجاح" -ForegroundColor $SuccessColor
        }
    }
} else {
    Write-Host "ℹ️  تم تخطي الرفع على GitHub" -ForegroundColor $InfoColor
}
Write-Host ""

# الخطوة 8: تعليمات تحديث السيرفر
Write-Host "================================================" -ForegroundColor $InfoColor
Write-Host "   🎉 تم النشر على GitHub بنجاح!   " -ForegroundColor $SuccessColor
Write-Host "================================================" -ForegroundColor $InfoColor
Write-Host ""
Write-Host "📋 الخطوات التالية لتحديث السيرفر:" -ForegroundColor $InfoColor
Write-Host ""
Write-Host "1️⃣  الاتصال بالسيرفر:" -ForegroundColor $InfoColor
Write-Host "   ssh user@rahamedical.com" -ForegroundColor $WarningColor
Write-Host ""
Write-Host "2️⃣  الانتقال لمجلد المشروع:" -ForegroundColor $InfoColor
Write-Host "   cd /path/to/raha-medical" -ForegroundColor $WarningColor
Write-Host ""
Write-Host "3️⃣  سحب التحديثات:" -ForegroundColor $InfoColor
Write-Host "   git pull origin main" -ForegroundColor $WarningColor
Write-Host ""
Write-Host "4️⃣  إعادة بناء Docker:" -ForegroundColor $InfoColor
Write-Host "   docker-compose down" -ForegroundColor $WarningColor
Write-Host "   docker-compose build --no-cache" -ForegroundColor $WarningColor
Write-Host "   docker-compose up -d" -ForegroundColor $WarningColor
Write-Host ""
Write-Host "5️⃣  التحقق من السجلات:" -ForegroundColor $InfoColor
Write-Host "   docker-compose logs -f" -ForegroundColor $WarningColor
Write-Host ""
Write-Host "================================================" -ForegroundColor $InfoColor
Write-Host ""

# فتح ملف الملخص
Write-Host "📄 فتح ملف الملخص..." -ForegroundColor $InfoColor
$summaryFile = Join-Path $currentPath "UPDATE_SUMMARY.md"
if (Test-Path $summaryFile) {
    Start-Process $summaryFile
    Write-Host "✅ تم فتح ملف الملخص" -ForegroundColor $SuccessColor
}

Write-Host ""
Write-Host "🎊 انتهى السكريبت بنجاح!" -ForegroundColor $SuccessColor
Write-Host ""

# سجل وقت التنفيذ
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Add-Content -Path "deployment_log.txt" -Value "$timestamp - Deployment completed successfully"

# انتظر قبل الإغلاق
Write-Host "اضغط أي مفتاح للخروج..." -ForegroundColor $InfoColor
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
