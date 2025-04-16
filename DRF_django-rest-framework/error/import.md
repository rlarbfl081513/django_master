## ✅ Django `rest_framework` import 오류 해결 정리

### ☑️ 문제 상황 요약
- `pip list`에서 `djangorestframework`가 분명히 설치되어 있음
- `INSTALLED_APPS`에도 `'rest_framework'`가 등록되어 있음
- 그런데도 `from rest_framework import serializers`에 노란 밑줄 경고 발생 (reportMissingImports)

---

### ☑️ 원인
> **VS Code가 현재 프로젝트의 가상환경(venv)을 인식하지 못하고 있었기 때문**

- VS Code는 내부적으로 "어떤 Python 인터프리터(환경)를 사용할지" 설정되어 있음
- 만약 가상환경을 인식 못 하면, 실제로 설치된 패키지(djangorestframework 등)를 VS Code가 찾지 못함
- 그래서 설치되어 있어도 에디터에서 **노란 밑줄**(`rest_framework를 찾을 수 없습니다`)이 뜨는 것

---

### ☑️ 해결 방법 (최종 정리)

1. **가상환경 먼저 활성화**
```bash
# PowerShell / CMD
.\venv\Scripts\activate

# Git Bash
source venv/Scripts/activate
```

2. **가상환경이 활성화된 상태에서 VS Code 실행**
```bash
code .
```

3. **VS Code 인터프리터 명시적으로 선택**
- `Ctrl + Shift + P` → `Python: Select Interpreter`
- 리스트에서 경로가 다음과 같은 항목을 선택:
```
./venv/Scripts/python.exe
```

4. (선택사항) `.vscode/settings.json` 설정으로 고정
```json
{
  "python.defaultInterpreterPath": "venv/Scripts/python.exe",
  "python.analysis.extraPaths": ["./venv/Lib/site-packages"],
  "python.analysis.diagnosticSeverityOverrides": {
    "reportMissingImports": "none"
  }
}
```

---

### ☑️ 결론
- 에러의 본질은 **코드나 설치 문제**가 아니라 VS Code가 **어떤 파이썬 환경을 보고 있는지**의 문제였다
- `Python: Select Interpreter`만 잘 해줘도 대부분 해결됨
- VS Code가 가상환경을 자동으로 못 잡을 수도 있기 때문에, **수동 선택**이 확실한 해결책!

---

🎉 이제 `from rest_framework import serializers` 도 더 이상 경고 없이 잘 인식됨!

