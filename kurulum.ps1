# ==============================================================================
# Görsel Ders Notu Üretim Sistemi — Otomatik Kurulum ve Doğrulama Betiği
# ==============================================================================
# Kullanım: PowerShell'de `.\kurulum.ps1` çalıştırın.

$ErrorActionPreference = "Stop"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "   GÖRSEL DERS NOTU SİSTEMİ — OTOMATİK KURULUM MOTORU    " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host ""

# 1. Python Kontrolü
Write-Host "[1/5] Python çalışma ortamı denetleniyor..." -ForegroundColor Yellow
try {
    $pyVer = python --version 2>&1
    Write-Host "  ✓ $pyVer algılandı." -ForegroundColor Green
} catch {
    Write-Host "  ✗ Python bulunamadı! Lütfen Python 3.10+ kurun (Add to PATH seçeneğini unutmayın)." -ForegroundColor Red
    Write-Host "    İpucu: 'winget install Python.Python.3.12' komutu ile kurabilirsiniz." -ForegroundColor Yellow
    exit 1
}

# 2. Node.js Kontrolü
Write-Host "[2/5] Node.js çalışma ortamı denetleniyor..." -ForegroundColor Yellow
try {
    $nodeVer = node --version 2>&1
    Write-Host "  ✓ Node.js $nodeVer algılandı." -ForegroundColor Green
} catch {
    Write-Host "  ✗ Node.js bulunamadı! Lütfen Node.js LTS kurun." -ForegroundColor Red
    Write-Host "    İpucu: 'winget install OpenJS.NodeJS.LTS' komutu ile kurabilirsiniz." -ForegroundColor Yellow
    exit 1
}

# 3. Python Paketlerinin Kurulumu
Write-Host "[3/5] Python paketleri kuruluyor (requirements.txt)..." -ForegroundColor Yellow
try {
    python -m pip install --upgrade pip --quiet
    python -m pip install -r requirements.txt
    Write-Host "  ✓ Python bağımlılıkları başarıyla yüklendi." -ForegroundColor Green
} catch {
    Write-Host "  ✗ Python paketleri yüklenirken hata oluştu." -ForegroundColor Red
    exit 1
}

# 4. Node.js Paketleri ve Playwright Chromium Kurulumu
Write-Host "[4/5] Node bağımlılıkları ve Chromium motoru kuruluyor..." -ForegroundColor Yellow
try {
    npm install
    npx playwright install chromium
    Write-Host "  ✓ Playwright ve Chromium başarıyla kuruldu." -ForegroundColor Green
} catch {
    Write-Host "  ✗ Playwright/Chromium kurulurken hata oluştu." -ForegroundColor Red
    exit 1
}

# 5. Uçtan Uca Test Derlemesi
Write-Host "[5/5] Örnek ders derlemesi test ediliyor (build.py ornek_ders)..." -ForegroundColor Yellow
try {
    python build.py ornek_ders
    Write-Host ""
    Write-Host "==========================================================" -ForegroundColor Green
    Write-Host "  ✓ TEBRİKLER! Kurulum başarıyla tamamlandı ve test edildi." -ForegroundColor Green
    Write-Host "  Sistem yeni ders notları üretmeye hazırdır.             " -ForegroundColor Green
    Write-Host "==========================================================" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Test derlemesi sırasında bir sorun oluştu." -ForegroundColor Red
    exit 1
}
