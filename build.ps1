# Build script para a dissertação (equivalente ao Makefile)
# Uso:
#   .\build.ps1          → compila apenas (atualização rápida)
#   .\build.ps1 -bib     → compilação completa com bibliografia
#   .\build.ps1 -clean   → remove arquivos temporários

param(
    [switch]$bib,
    [switch]$clean
)

$ARTIGO = "tese"
$DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
Push-Location $DIR

if ($clean) {
    Write-Host "Limpando arquivos temporários..." -ForegroundColor Yellow
    Remove-Item -ErrorAction SilentlyContinue @(
        "*.log", "*.aux", "*.toc", "*.lof", "*.lot", "*.loa",
        "*.blg", "*.bbl", "*.ind", "*.ilg", "*.idx",
        "*.glo", "*.gls", "*.out", "*.synctex.gz"
    )
    Write-Host "Pronto." -ForegroundColor Green
    Pop-Location
    exit 0
}

function Run-PDFLaTeX {
    Write-Host "Executando pdflatex $ARTIGO..." -ForegroundColor Cyan
    pdflatex -interaction=nonstopmode -file-line-error "$ARTIGO.tex"
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERRO no pdflatex (código $LASTEXITCODE). Verifique o log." -ForegroundColor Red
        Pop-Location
        exit $LASTEXITCODE
    }
}

if ($bib) {
    Write-Host "=== Compilação completa com bibliografia ===" -ForegroundColor Magenta
    Run-PDFLaTeX
    Write-Host "Executando bibtex $ARTIGO..." -ForegroundColor Cyan
    bibtex "$ARTIGO"
    Run-PDFLaTeX
    Run-PDFLaTeX
    Run-PDFLaTeX
} else {
    Write-Host "=== Compilação rápida ===" -ForegroundColor Magenta
    Run-PDFLaTeX
}

Write-Host "=== PDF gerado: $ARTIGO.pdf ===" -ForegroundColor Green
Pop-Location
