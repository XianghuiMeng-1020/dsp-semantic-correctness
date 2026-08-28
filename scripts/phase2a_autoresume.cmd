@echo off
REM Resume Phase 2A after a reboot / crash. Safe to run if already complete.
set ROOT=F:\ICASSP\project_a_public_release
set LOG=%ROOT%\results\icassp_10of10_hardening\phase2a\autoresume.log
if exist "%ROOT%\results\icassp_10of10_hardening\phase2a\headline.json" (
  if not exist "%ROOT%\results\icassp_10of10_hardening\phase2a\_checkpoint.jsonl" (
    echo %DATE% %TIME% already complete>>"%LOG%"
    exit /b 0
  )
)
cd /d "%ROOT%"
echo %DATE% %TIME% resume start>>"%LOG%"
set PYTHONUNBUFFERED=1
python -m experiments.icassp_10of10_hardening.phase2a.run_all >>"%LOG%" 2>&1
echo %DATE% %TIME% resume exit %ERRORLEVEL%>>"%LOG%"
exit /b %ERRORLEVEL%
