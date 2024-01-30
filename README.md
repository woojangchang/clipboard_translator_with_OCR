# 클립보드 번역기
자세한 내용은 링크를 참고하세요.
https://boksup.tistory.com/20

# 주의사항
python 언어에 대한 이해가 부족할 때 작성한 코드라 많이 스파게티입니다.
버그나 코드를 말끔하게 수정해주시면 매우 감사하겠습니다...


# pyinstaller를 통한 exe 만들기
`pyinstaller -w -F --hidden-import=jaraco.clipboard.Windows --icon=icon.ico --add-data "icon.ico;." --add-data "img3.png;." --version-file=VersionOCR.txt "Clipboard Translator with OCR v2.081.py"`

