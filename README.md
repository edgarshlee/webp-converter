# WebP Converter

**마음에 드는 이미지를, 내 바탕화면으로.**

WebP 이미지를 PNG 또는 JPG로 바꾸는 작은 Windows 데스크톱 도구입니다.
여러 이미지를 한 번에 선택하고, 형식과 저장 폴더를 정하면 내 컴퓨터에서 바로 변환합니다.

## 만들게 된 이유

인터넷에서 마음에 드는 배경화면을 발견해 저장했는데, 파일 확장자가 `.webp`였습니다.
이미지는 잘 보이지만 Windows 10에서 바탕화면 배경으로 바로 지정하려니 불편했습니다.
배경화면 한 장을 쓰려고 변환 사이트에 파일을 올리거나 이미지 편집기를 여는 과정도 번거로웠습니다.

그래서 **WebP를 PNG나 JPG로 간단하게 바꿔서 배경화면으로 쓰자**는 생각으로 만들었습니다.
거창한 편집 기능보다, 파일을 고르고 변환해서 바로 사용할 수 있는 흐름에 집중한 개인 프로젝트입니다.

> Windows 10에서 WebP를 배경화면으로 바로 사용하기 어려웠던 경험이 출발점입니다.
> Windows의 모든 버전에서 PNG/JPG만 지원한다는 의미는 아닙니다. 지원 형식과 메뉴는 Windows 버전 및 사용하는 앱에 따라 달라질 수 있습니다.

## 주요 기능

- **WebP → PNG / JPG**: 확장자만 바꾸는 것이 아니라 이미지를 실제로 다시 저장합니다.
- **여러 파일 일괄 변환**: 파일 선택 창에서 여러 WebP를 함께 선택할 수 있습니다.
- **PNG 투명도 유지**: 원본의 투명한 영역을 유지합니다.
- **JPG 품질·배경색 선택**: 품질을 1~100으로 조절하고 투명 영역을 채울 색을 정합니다.
- **원본과 기존 결과 보호**: 원본은 수정하지 않으며, 같은 이름이 있으면 `_1`, `_2`를 붙입니다.
- **파일별 오류 처리**: 손상된 이미지가 있어도 나머지 파일은 계속 변환합니다.
- **로컬 처리**: 변환 과정에서 이미지를 서버로 전송하지 않습니다.

## 설치와 실행

### 준비물

- Python 3.10 이상 — Windows 설치 시 **Tcl/Tk 및 IDLE** 구성 요소를 포함하세요.
- 의존성 설치를 위한 인터넷 연결. 설치가 끝나면 이미지 변환은 오프라인에서도 가능합니다.

### 처음 실행하기

저장소를 내려받고 PowerShell에서 다음 명령을 실행합니다.

```powershell
git clone https://github.com/edgarshlee/webp-converter.git
cd webp-converter
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python app.py
```

Git이 없다면 GitHub의 **Code → Download ZIP**으로 다운로드한 뒤 압축을 풀고,
해당 폴더에서 `python -m venv .venv`부터 실행하면 됩니다.
가상환경 활성화 없이 실행하므로 PowerShell 실행 정책을 변경할 필요가 없습니다.

### 다음부터 실행하기

프로젝트 폴더에서 아래 명령만 실행합니다.

```powershell
.\.venv\Scripts\python app.py
```

## WebP를 PNG로 바꿔 배경화면으로 사용하기

1. 프로그램에서 **WebP 파일 추가**를 누릅니다.
2. 변환할 `.webp` 파일을 선택합니다. `Ctrl` 또는 `Shift`로 여러 파일을 선택할 수 있습니다.
3. **출력 형식**을 `PNG`로 선택합니다. 기본값도 PNG입니다.
4. **저장 폴더**를 눌러 결과를 보관할 폴더를 지정합니다.
5. **변환 시작**을 누르고 하단의 성공·실패 개수를 확인합니다.
6. 저장된 PNG 파일을 파일 탐색기에서 찾습니다.
7. 파일을 우클릭해 **바탕 화면 배경으로 설정**을 선택합니다.

우클릭 메뉴에 해당 항목이 없다면 Windows 10의 **설정 → 개인 설정 → 배경**에서
배경을 **사진**으로 선택하고 **찾아보기**로 변환된 파일을 지정하세요.
이미지가 잘리면 맞춤 설정에서 **맞춤** 또는 **채우기**를 조절해 보세요.
이 프로그램은 변환 파일을 저장하며 Windows 배경화면을 자동으로 변경하지는 않습니다.

## PNG와 JPG 중 무엇을 선택할까요?

| 형식 | 이런 경우에 사용하세요 | 참고 |
| --- | --- | --- |
| PNG | 추가 손실 압축 없이 저장하고 싶거나 투명도가 필요한 이미지 | JPG보다 파일이 커질 수 있습니다. |
| JPG | 사진 배경화면을 작은 용량으로 저장하고 싶은 경우 | 손실 압축이며 투명한 부분은 선택한 배경색으로 채웁니다. |

JPG 품질 기본값은 **90**, 배경색 기본값은 **흰색**입니다.
JPG 품질과 배경색 설정은 PNG 출력에는 적용되지 않습니다.
PNG로 바꿔도 원본 WebP에서 이미 손실된 디테일이 복구되지는 않습니다.

## 알아둘 점

- 움직이는 WebP는 **첫 번째 프레임만** 정지 이미지로 저장합니다.
- 크기 조절이나 자르기 기능은 없습니다. EXIF 회전 방향을 적용하므로 가로·세로가 바뀔 수 있습니다.
- EXIF 방향은 적용하지만 원본 메타데이터와 색상 프로파일의 보존은 보장하지 않습니다.
- 대용량 이미지는 메모리와 처리 시간이 더 필요할 수 있습니다.
- 창을 닫으려면 진행 중인 변환이 끝날 때까지 기다려 주세요.

## 문제 해결

### `python`을 찾을 수 없거나 Microsoft Store가 열려요

Python 설치 여부와 PATH 설정을 확인하세요. Python Launcher가 설치되어 있다면
`python -m venv .venv` 대신 `py -m venv .venv`로 가상환경을 만들 수 있습니다.

### `No module named PIL` 오류가 나요

앱을 실행하는 가상환경에 의존성을 설치하세요.

```powershell
.\.venv\Scripts\python -m pip install -r requirements.txt
```

### `init.tcl` 또는 `tkinter` 오류가 나요

Python의 Tcl/Tk 구성 요소가 없거나 런타임 경로에 문제가 있는 경우입니다.
Tcl/Tk를 포함한 정식 Python 설치를 확인한 뒤 해당 Python으로 가상환경을 새로 만드세요.

### 파일 변환이 실패해요

파일이 실제 WebP 이미지인지, 손상되지 않았는지, 저장 폴더에 쓰기 권한이 있는지 확인하세요.
다른 이미지의 확장자만 `.webp`로 바꾼 파일은 변환 대상으로 인정하지 않습니다.

## 개발과 테스트

Python, Tkinter, Pillow로 구성되어 있습니다.

```text
app.py                       데스크톱 UI와 백그라운드 일괄 처리
converter.py                 이미지 검증 및 PNG/JPG 변환
requirements.txt             Pillow 의존성
test_converter.py            변환 테스트
.github/workflows/tests.yml   Windows 자동 테스트
```

```powershell
.\.venv\Scripts\python -m unittest -v
```

테스트는 PNG 투명도, JPG 출력, 파일명 충돌, 잘못된 입력과 손상 파일,
움직이는 WebP의 첫 프레임 처리를 검증합니다. GUI 조작 전체를 검증하는 테스트는 아닙니다.

## 선택: Windows 실행 파일 만들기

Windows 환경에서 아래 명령으로 Python 없이 실행할 수 있는 파일을 만들 수 있습니다.

```powershell
.\.venv\Scripts\python -m pip install pyinstaller
.\.venv\Scripts\python -m PyInstaller --onefile --windowed --name WebPConverter app.py
```

생성 위치는 `dist/WebPConverter.exe`입니다. 이 저장소에는 소스 코드가 포함되어 있으며,
실행 파일 빌드는 별도 단계입니다.

## 참고 자료

- [Microsoft: Windows 바탕 화면 배경 변경](https://support.microsoft.com/en-us/windows/experience/personalization/change-the-desktop-background-in-windows)
- [Pillow: 이미지 파일 형식](https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html)
